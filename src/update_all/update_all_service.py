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
import configparser
import dataclasses
import datetime
import io
import json
import re
import sys
import time
from functools import cached_property
from typing import List, Tuple

from update_all.constants import K_MAIN_UPDATER, K_JOTEGO_UPDATER, K_UNOFFICIAL_UPDATER, K_LLAPI_UPDATER, \
    K_ARCADE_OFFSET_DOWNLOADER, K_ARCADE_ROMS_DB_DOWNLOADER, K_TTY2OLED_FILES_DOWNLOADER, K_I2C2OLED_FILES_DOWNLOADER, \
    K_MISTERSAM_FILES_DOWNLOADER, K_BIOS_GETTER, K_NAMES_TXT_UPDATER, UPDATE_ALL_VERSION, DOWNLOADER_INI_STANDARD_PATH, \
    DOWNLOADER_URL, ARCADE_ORGANIZER_URL, FILE_update_all_log, FILE_mister_downloader_needs_reboot
from update_all.countdown import Countdown, CountdownImpl, CountdownOutcome
from update_all.databases import db_distribution_mister_by_encc_forks, db_jtcores_by_download_beta_cores, \
    DB_THEYPSILON_UNOFFICIAL_DISTRIBUTION, DB_LLAPI_FOLDER, DB_ARCADE_OFFSET_FOLDER, DB_ARCADE_ROMS, DB_TTY2OLED_FILES, \
    DB_I2C2OLED_FILES, DB_MISTERSAM_FILES, DB_BIOS, db_names_txt_by_locale, Database
from update_all.local_store import LocalStoreProvider
from update_all.logger import Logger
from update_all.os_utils import OsUtils, LinuxOsUtils
from update_all.store_migrator import StoreMigrator
from update_all.migrations import migrations
from update_all.local_repository import LocalRepository, LocalRepositoryProvider
from update_all.file_system import FileSystemFactory, FileSystem
from update_all.config import ConfigReader, ConfigProvider


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
        local_store_provider = LocalStoreProvider()
        os_utils = LinuxOsUtils(config_provider=config_provider, logger=self._logger)
        return UpdateAllService(config_reader, config_provider, local_store_provider, self._logger, local_repository, store_migrator, file_system, os_utils, CountdownImpl())


class UpdateAllService:
    def __init__(self, config_reader: ConfigReader, config_provider: ConfigProvider, local_store_provider: LocalStoreProvider, logger: Logger, local_repository: LocalRepository, store_migrator: StoreMigrator, file_system: FileSystem, os_utils: OsUtils, countdown: Countdown):
        self._config_reader = config_reader
        self._config_provider = config_provider
        self._local_store_provider = local_store_provider
        self._logger = logger
        self._local_repository = local_repository
        self._store_migrator = store_migrator
        self._file_system = file_system
        self._os_utils = os_utils
        self._countdown = countdown
        self._exit_code = 0
        self._error_reports: List[str] = []

    def full_run(self) -> int:
        self._show_intro()
        self._read_config()
        self._initialize_store()
        self._run_settings_screen_countdown()
        self._run_downloader()
        self._run_arcade_organizer()
        self._run_linux_update()
        self._cleanup()
        self._show_outro()
        self._reboot_if_needed()
        return self._exit_code

    @cached_property
    def _candidate_databases(self) -> list[Tuple[str, Database]]:
        config = self._config_provider.get()
        return [
            (K_MAIN_UPDATER, db_distribution_mister_by_encc_forks(config.encc_forks)),
            (K_JOTEGO_UPDATER, db_jtcores_by_download_beta_cores(config.download_beta_cores)),
            (K_UNOFFICIAL_UPDATER, DB_THEYPSILON_UNOFFICIAL_DISTRIBUTION),
            (K_LLAPI_UPDATER, DB_LLAPI_FOLDER),
            (K_ARCADE_OFFSET_DOWNLOADER, DB_ARCADE_OFFSET_FOLDER),
            (K_ARCADE_ROMS_DB_DOWNLOADER, DB_ARCADE_ROMS),
            (K_TTY2OLED_FILES_DOWNLOADER, DB_TTY2OLED_FILES),
            (K_I2C2OLED_FILES_DOWNLOADER, DB_I2C2OLED_FILES),
            (K_MISTERSAM_FILES_DOWNLOADER, DB_MISTERSAM_FILES),
            (K_BIOS_GETTER, DB_BIOS),
            (K_NAMES_TXT_UPDATER, db_names_txt_by_locale(config.names_region, config.names_char_code, config.names_sort_code)),
        ]

    @cached_property
    def _active_databases(self) -> list[Database]:
        config = self._config_provider.get()
        return [db for var, db in self._candidate_databases if dataclasses.asdict(config)[var.lower()]]

    def _show_intro(self) -> None:
        self._logger.print("Executing 'Update All' script")
        self._logger.print("The All-in-One Updater for MiSTer")
        self._logger.print(f"Version {UPDATE_ALL_VERSION}")
        self._logger.print()

    def _read_config(self) -> None:
        self._logger.print(f"Reading INI file '{self._config_reader.ini_path}'")
        config, is_file_read = self._config_reader.read_config()
        if is_file_read:
            self._logger.print('OK.')
        else:
            self._logger.print('Not found.')

        self._config_provider.initialize(config)
        self._logger.print()

    def _initialize_store(self) -> None:
        self._local_store_provider.initialize(self._local_repository.load_store())

    def _run_settings_screen_countdown(self) -> None:
        self._print_sequence()
        outcome = self._countdown.execute_count(15)
        if outcome == CountdownOutcome.SETTINGS_SCREEN:
            self._load_settings_screen()
            self._print_sequence()
        elif outcome == CountdownOutcome.CONTINUE:
            pass
        else:
            raise NotImplementedError('No possible countdown outcome')

    def _run_downloader(self) -> None:
        if len(self._active_databases) == 0:
            return

        self._draw_separator()
        self._logger.print('Running MiSTer Downloader')
        self._write_downloader_ini()

        content = self._os_utils.download(DOWNLOADER_URL)
        temp_file = self._file_system.temp_file_by_id('downloader.sh')
        self._file_system.write_file_bytes(temp_file.name, content)

        self._logger.print()

        return_code = self._os_utils.execute_process(temp_file.name, {
            'DOWNLOADER_INI_PATH': DOWNLOADER_INI_STANDARD_PATH,
            'ALLOW_REBOOT': '0',
            'CURL_SSL': self._config_provider.get().curl_ssl,
            'UPDATE_LINUX': 'false' if self._config_provider.get().arcade_organizer else 'true',
            'LOGFILE': f'{self._config_provider.get().base_path}/Scripts/.config/downloader/downloader1.log'
        })

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
            'INI_FILE': f'{self._config_provider.get().base_path}/Scripts/update_arcade-organizer.ini'
        })

        if return_code != 0:
            self._exit_code = 1
            self._error_reports.append('Arcade Organizer')

        self._logger.print()
        self._logger.print("FINISHED: Arcade Organizer")

    def _run_linux_update(self) -> None:
        if len(self._active_databases) == 0 or not self._config_provider.get().arcade_organizer:
            return

        self._draw_separator()
        self._logger.print('Running Linux Update')
        self._logger.print()

        temp_file = self._file_system.temp_file_by_id('downloader.sh')
        return_code = self._os_utils.execute_process(temp_file.name, {
            'DOWNLOADER_INI_PATH': DOWNLOADER_INI_STANDARD_PATH,
            'ALLOW_REBOOT': '0',
            'CURL_SSL': self._config_provider.get().curl_ssl,
            'UPDATE_LINUX': 'only',
            'LOGFILE': f'{self._config_provider.get().base_path}/Scripts/.config/downloader/downloader2.log'
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
            self._logger.print(f"Update All {UPDATE_ALL_VERSION} finished. Your MiSTer has been updated successfully!")

        run_time = str(datetime.timedelta(seconds=time.time() - self._config_provider.get().start_time))[0:-4]

        self._logger.print()
        self._logger.print(f"Run time: {run_time}s")
        self._logger.print()
        self._logger.print(f"Full log for more details: {FILE_update_all_log}")
        self._logger.print()

    def _reboot_if_needed(self) -> None:
        if not self._file_system.is_file(FILE_mister_downloader_needs_reboot):
            return

        if not self._config_provider.get().allow_reboot:
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
        for db in self._active_databases:
            self._logger.print(f'- {db.title}')
        if self._config_provider.get().arcade_organizer:
            self._logger.print('- Arcade Organizer')
        self._logger.print()

    def _load_settings_screen(self) -> None:
        pass

    def _write_downloader_ini(self) -> None:
        ini_path = DOWNLOADER_INI_STANDARD_PATH
        ini: dict[str, dict[str, str]] = dict()
        before = ''
        try:
            ini_contents = self._file_system.read_file_contents(ini_path)
            parser = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
            parser.read_string(ini_contents)
            ini = {header.lower(): {k.lower(): v for k, v in section.items()} for header, section in parser.items() if
                   header.lower() != 'default'}
            before = json.dumps(ini)
        except Exception as e:
            self._logger.print(f'Could not read ini file {ini_path}')
            self._logger.debug(e)

        db_ids = {db.db_id for _, db in self._candidate_databases}

        for _, db in self._candidate_databases:
            if db in self._active_databases:
                if db.db_id not in ini:
                    ini[db.db_id] = {}
                ini[db.db_id]['db_url'] = db.db_url
            elif db.db_id in ini:
                del ini[db.db_id]

        after = json.dumps(ini)

        if before == after:
            return

        mister_section = ''
        nomister_section = ''
        pre_section = ''

        if self._file_system.is_file(ini_path):
            header_regex = re.compile('\s*\[([-_a-z0-9]+)\].*', re.I)
            ini_contents = io.StringIO(self._file_system.read_file_contents(ini_path))

            no_section = 0
            other_section = 1
            common_section = 2

            state = no_section

            for line in ini_contents.readlines():
                match = header_regex.match(line)

                section: str
                if match is not None:
                    section = match.group(1).lower()
                    if section in db_ids:
                        state = common_section
                    else:
                        state = other_section

                if state == no_section:
                    pre_section += line
                elif state == common_section:
                    pass
                elif state == other_section:
                    if section in ini:
                        ini.pop(section)

                    if section == 'mister':
                        mister_section += line
                    else:
                        nomister_section += line
                else:
                    raise Exception("Wrong state: " + str(state))

        parser = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        for header, section_id in ini.items():
            parser[header] = section_id

        with io.StringIO() as ss:
            if pre_section != '':
                ss.write(pre_section.strip() + '\n\n')
            if mister_section != '':
                ss.write(mister_section.strip() + '\n\n')
            parser.write(ss)
            if nomister_section != '':
                ss.write(nomister_section.strip() + '\n\n')
            ss.seek(0)
            ini_contents = ss.read()
            self._file_system.write_file_contents(ini_path, ini_contents)

        self._logger.print('Written changes on ' + ini_path)

    def _draw_separator(self) -> None:
        self._logger.print()
        self._logger.print()
        self._logger.print("################################################################################")
        self._logger.print("#==============================================================================#")
        self._logger.print("################################################################################")
        self._logger.print()
        self._os_utils.sleep(1.0)
