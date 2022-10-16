# Copyright (c) 2022 José Manuel Barroso Galindo <theypsilon@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You can download the latest version of this tool from:
# https://github.com/theypsilon-test/ua2
import datetime
import sys
import time
from typing import List

from update_all.cli_output_formatting import CLEAR_SCREEN
from update_all.config import Config, ConfigProvider
from update_all.constants import UPDATE_ALL_VERSION, DOWNLOADER_INI_STANDARD_PATH, \
    DOWNLOADER_URL, ARCADE_ORGANIZER_URL, FILE_update_all_log, FILE_mister_downloader_needs_reboot, MEDIA_FAT, \
    ARCADE_ORGANIZER_INI, MISTER_DOWNLOADER_VERSION, FILE_downloader_temp_ini
from update_all.countdown import Countdown, CountdownImpl, CountdownOutcome
from update_all.databases import active_databases
from update_all.downloader_ini_repository import DownloaderIniRepository
from update_all.other import Checker
from update_all.logger import Logger
from update_all.os_utils import OsUtils, LinuxOsUtils
from update_all.settings_screen import SettingsScreen
from update_all.settings_screen_standard_printer import SettingsScreenStandardPrinter
from update_all.settings_screen_trivial_printer import SettingsScreenTrivialPrinter
from update_all.store_migrator import StoreMigrator
from update_all.migrations import migrations
from update_all.local_repository import LocalRepository, LocalRepositoryProvider
from update_all.file_system import FileSystemFactory, FileSystem
from update_all.config_reader import ConfigReader


class UpdateAllServiceFactory:
    def __init__(self, logger: Logger, local_repository_provider: LocalRepositoryProvider):
        self._logger = logger
        self._local_repository_provider = local_repository_provider

    def create(self, env: dict[str, str]):
        config_reader = ConfigReader(self._logger, env)
        config_provider = ConfigProvider()
        store_migrator = StoreMigrator(migrations(), self._logger)
        file_system = FileSystemFactory(config_provider, {}, self._logger).create_for_system_scope()
        local_repository = LocalRepository(config_provider, self._logger, file_system, store_migrator)
        self._local_repository_provider.initialize(local_repository)
        os_utils = LinuxOsUtils(config_provider=config_provider, logger=self._logger)
        downloader_ini_repository = DownloaderIniRepository(self._logger, file_system=file_system, os_utils=os_utils)
        checker = Checker(file_system=file_system)
        return UpdateAllService(
            config_reader,
            config_provider,
            downloader_ini_repository,
            self._logger,
            local_repository,
            store_migrator,
            file_system,
            os_utils,
            CountdownImpl(),
            SettingsScreen(
                logger=self._logger,
                config_provider=config_provider,
                file_system=file_system,
                downloader_ini_repository=downloader_ini_repository,
                os_utils=os_utils,
                settings_screen_printer=SettingsScreenStandardPrinter(),
                checker=checker,
                local_repository=local_repository
            ),
            checker=checker
        )


class UpdateAllService:
    def __init__(self, config_reader: ConfigReader, config_provider: ConfigProvider, downloader_ini_repository: DownloaderIniRepository, logger: Logger, local_repository: LocalRepository, store_migrator: StoreMigrator, file_system: FileSystem, os_utils: OsUtils, countdown: Countdown, settings_screen: SettingsScreen, checker: Checker):
        self._config_reader = config_reader
        self._config_provider = config_provider
        self._downloader_ini_repository = downloader_ini_repository
        self._logger = logger
        self._local_repository = local_repository
        self._store_migrator = store_migrator
        self._file_system = file_system
        self._os_utils = os_utils
        self._countdown = countdown
        self._settings_screen = settings_screen
        self._checker = checker
        self._exit_code = 0
        self._error_reports: List[str] = []

    def full_run(self) -> int:
        self._read_config()
        self._show_intro()
        self._run_settings_screen_countdown()
        self._tweak_not_mister_config()
        self._run_downloader()
        self._run_arcade_organizer()
        self._run_linux_update()
        self._cleanup()
        self._show_outro()
        self._reboot_if_needed()
        return self._exit_code

    def _show_intro(self) -> None:
        self._logger.print()
        self._logger.print(f"                        -------- Update All {UPDATE_ALL_VERSION} ---------                        ")
        self._logger.print(f"                        The All-in-One Updater for MiSTer")
        self._logger.print("                        ---------------------------------")
        self._logger.print(f"                          - Powered by Downloader {MISTER_DOWNLOADER_VERSION} -")
        self._logger.print()
        if self._checker.available_code < 2:
            self._logger.print()
            self._logger.print("               ╔═════════════════════════════════════════════════╗              ")
            self._logger.print("               ║  Become a patron to unlock exclusive features!  ║              ")
            self._logger.print("               ║           www.patreon.com/theypsilon            ║              ")
            self._logger.print("               ╚═════════════════════════════════════════════════╝              ")
            self._os_utils.sleep(2.0)
        else:
            self._logger.print()
            self._logger.print("                    ╔═══════════════════════════════════════╗                   ")
            self._logger.print("                    ║  Thank you so much for your support!  ║                   ")
            self._logger.print("                    ╚═══════════════════════════════════════╝                   ")

        self._logger.print()
        self._logger.print('Reading downloader.ini')
        self._logger.print()

    def _read_config(self) -> None:
        config = Config()
        self._config_reader.fill_config_with_environment(config)
        self._config_provider.initialize(config)
        self._downloader_ini_repository.transition_from_update_all_1(config)
        self._config_reader.fill_config_with_ini_files(config, self._file_system)


    def _run_settings_screen_countdown(self) -> None:
        self._print_sequence()
        outcome = self._countdown.execute_count(15)
        if outcome == CountdownOutcome.SETTINGS_SCREEN:
            self._settings_screen.load_main_menu()
            self._logger.print(CLEAR_SCREEN, end='')
            self._print_sequence()
        elif outcome == CountdownOutcome.CONTINUE:
            pass
        else:
            raise NotImplementedError('No possible countdown outcome')

    def _tweak_not_mister_config(self):
        config = self._config_provider.get()
        if config.not_mister:
            self._logger.debug('Not MiSTer environment!')
            config.arcade_organizer = False
            config.update_linux = False
            config.autoreboot = False

    def _run_downloader(self) -> None:
        config = self._config_provider.get()
        if len(active_databases(config)) == 0:
            return

        self._draw_separator()
        self._logger.print('Running MiSTer Downloader')

        if config.temporary_downloader_ini:
            self._downloader_ini_repository.write_downloader_ini(config, FILE_downloader_temp_ini)
            self._logger.print(f'Written temporary {FILE_downloader_temp_ini} file.')

        content = self._os_utils.download(DOWNLOADER_URL)
        temp_file = self._file_system.temp_file_by_id('downloader.sh')
        self._file_system.write_file_bytes(temp_file.name, content)

        self._logger.print()

        update_linux = self._config_provider.get().update_linux
        arcade_organizer = self._config_provider.get().arcade_organizer

        if update_linux and arcade_organizer:
            update_linux = False

        env = {
            'DOWNLOADER_INI_PATH': FILE_downloader_temp_ini if config.temporary_downloader_ini else DOWNLOADER_INI_STANDARD_PATH,
            'ALLOW_REBOOT': '0',
            'CURL_SSL': self._config_provider.get().curl_ssl,
            'UPDATE_LINUX': 'true' if update_linux else 'false',
            'LOGFILE': f'{self._config_provider.get().base_path}/Scripts/.config/downloader/downloader1.log'
        }

        base_path = self._config_provider.get().base_path
        if base_path != MEDIA_FAT:
            env['DEFAULT_BASE_PATH'] = base_path

        return_code = self._os_utils.execute_process(temp_file.name, env)

        if return_code != 0:
            self._exit_code = 1
            self._error_reports.append('Scripts/.config/downloader/downloader1.log')

    def _run_arcade_organizer(self) -> None:
        if not self._config_provider.get().arcade_organizer:
            return

        self._draw_separator()
        self._logger.print("Running Arcade Organizer")
        self._logger.print()

        content = self._os_utils.download(ARCADE_ORGANIZER_URL)
        temp_file = self._file_system.temp_file_by_id('arcade_organizer.sh')
        self._file_system.write_file_bytes(temp_file.name, content)

        return_code = self._os_utils.execute_process(temp_file.name, {
            'SSL_SECURITY_OPTION': self._config_provider.get().curl_ssl,
            'INI_FILE': f'{self._config_provider.get().base_path}/{ARCADE_ORGANIZER_INI}'
        })

        if return_code != 0:
            self._exit_code = 1
            self._error_reports.append('Arcade Organizer')

        self._logger.print()
        self._logger.print("FINISHED: Arcade Organizer")

    def _run_linux_update(self) -> None:
        config = self._config_provider.get()
        if not config.update_linux:
            return

        if len(active_databases(config)) == 0 or not config.arcade_organizer:
            return

        self._draw_separator()
        self._logger.print('Running Linux Update')
        self._logger.print()

        temp_file = self._file_system.temp_file_by_id('downloader.sh')
        return_code = self._os_utils.execute_process(temp_file.name, {
            'DOWNLOADER_INI_PATH': FILE_downloader_temp_ini if config.temporary_downloader_ini else DOWNLOADER_INI_STANDARD_PATH,
            'ALLOW_REBOOT': '0',
            'CURL_SSL': config.curl_ssl,
            'UPDATE_LINUX': 'only',
            'LOGFILE': f'{config.base_path}/Scripts/.config/downloader/downloader2.log'
        })

        if return_code != 0:
            self._exit_code = 1
            self._error_reports.append('Scripts/.config/downloader/downloader2.log')

    def _cleanup(self) -> None:
        self._file_system.clean_temp_files_with_ids()

    def _show_outro(self) -> None:
        self._draw_separator()

        if len(self._error_reports):
            self._logger.print("There were some errors in the Updaters.")
            self._logger.print("Therefore, MiSTer hasn't been fully updated.")
            self._logger.print()
            self._logger.print("Check these logs from the Updaters that failed:")
            for log_file in self._error_reports:
                self._logger.print(f" - {log_file}")

            self._logger.print()
            self._logger.print("Maybe a network problem?")
            self._logger.print("Check your connection and then run this script again.")
        else:
            self._logger.print(f"Update All {UPDATE_ALL_VERSION} by theypsilon. Your MiSTer has been updated successfully!")

        run_time = str(datetime.timedelta(seconds=time.time() - self._config_provider.get().start_time))[0:-4]

        self._logger.print()
        self._logger.print(f"Run time: {run_time}s")
        self._logger.print()
        self._logger.print(f"Full log for more details: {FILE_update_all_log}")
        self._logger.print()

    def _reboot_if_needed(self) -> None:
        if self._config_provider.get().not_mister:
            return

        if not self._file_system.is_file(FILE_mister_downloader_needs_reboot):
            return

        if not self._config_provider.get().autoreboot:
            self._logger.print('You should reboot')
            self._logger.print()
            return

        self._logger.print()
        self._logger.print("Rebooting in 10 seconds...")
        sys.stdout.flush()
        self._os_utils.sleep(2)
        self._logger.finalize()
        sys.stdout.flush()
        self._os_utils.sleep(4)
        self._os_utils.sync()
        self._os_utils.sleep(4)
        self._os_utils.sync()
        self._os_utils.sleep(30)
        self._os_utils.reboot()

    def _print_sequence(self) -> None:
        self._logger.print('Sequence:')
        config = self._config_provider.get()
        for db in active_databases(config):
            self._logger.print(f'- {db.title}')
        if config.arcade_organizer:
            self._logger.print('- Arcade Organizer')
        self._logger.print()

    def _draw_separator(self) -> None:
        self._logger.print()
        self._logger.print()
        self._logger.print("################################################################################")
        self._logger.print("#==============================================================================#")
        self._logger.print("################################################################################")
        self._logger.print()
        self._os_utils.sleep(1.0)
