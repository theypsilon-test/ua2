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
import curses
import hashlib
import os
from functools import cached_property
from pathlib import Path
from typing import Dict, Callable

from update_all.config import ConfigProvider, load_ini_config_with_no_section, Config
from update_all.constants import ARCADE_ORGANIZER_INI, FILE_update_all_ini, \
    UPDATE_ALL_PATREON_KEY_PATH, UPDATE_ALL_PATREON_KEY_MD5Q0, UPDATE_ALL_PATREON_KEY_SIZE, FILE_MiSTer, \
    TEST_UNSTABLE_SPINNER_FIRMWARE_MD5, DOWNLOADER_URL, FILE_MiSTer_ini, ARCADE_ORGANIZER_URL
from update_all.downloader_ini_repository import DownloaderIniRepository
from update_all.file_system import FileSystem
from update_all.logger import Logger
from update_all.os_utils import OsUtils
from update_all.settings_screen_model import settings_screen_model
from update_all.settings_screen_basic_theme import SettingsScreenBasicTheme
from update_all.ui_engine import run_ui_engine, Ui, UiComponent
from update_all.ui_model_utilities import gather_default_values, list_variables_with_group, dynamic_convert_string


class SettingsScreen(UiComponent):
    def __init__(self, logger: Logger, config_provider: ConfigProvider, file_system: FileSystem,
                 downloader_ini_repository: DownloaderIniRepository, os_utils: OsUtils):
        self._logger = logger
        self._config_provider = config_provider
        self._file_system = file_system
        self._downloader_ini_repository = downloader_ini_repository
        self._os_utils = os_utils
        self._original_firmware = None

    def load_main_menu(self) -> None:
        run_ui_engine('main_menu', settings_screen_model(), [self], SettingsScreenBasicTheme())

    def initialize_ui(self, ui: Ui) -> None:
        ui.set_value('needs_save', 'false')

        config = self._config_provider.get()
        for variable in self._all_config_variables:
            ui.set_value(variable, str(getattr(config, variable)).lower())

        arcade_organizer_ini_path = Path(f'{config.base_path}/{ARCADE_ORGANIZER_INI}')
        arcade_organizer_ini = load_ini_config_with_no_section(self._logger, arcade_organizer_ini_path)

        ao_variables = list_variables_with_group(settings_screen_model(), "ao_ini")
        variable_defaults = gather_default_values(settings_screen_model())

        for variable, rename in ao_variables.items():
            value = arcade_organizer_ini.get_string(rename, str(variable_defaults[variable]).lower())
            ui.set_value(variable, value)

    def initialize_effects(self, ui: Ui, effects: Dict[str, Callable[[], None]]) -> None:
        effects['calculate_needs_save'] = lambda effect: self.calculate_needs_save(ui)
        effects['calculate_patrons'] = lambda effect: self.calculate_patrons(ui)
        effects['test_unstable_spinner'] = lambda effect: self.test_unstable_spinner(ui)
        effects['play_bad_apple'] = lambda effect: self.play_bad_apple(ui)
        effects['save'] = lambda effect: self.save(ui)
        effects['copy_ui_options_to_current_config'] = lambda effect: self.copy_ui_options_to_current_config(ui)
        effects['calculate_file_exists'] = lambda effect: self.calculate_file_exists(ui, effect)
        effects['remove_file'] = lambda effect: self.remove_file(ui, effect)
        effects['calculate_arcade_organizer_folders'] = lambda effect: self.calculate_arcade_organizer_folders(ui)
        effects['clean_arcade_organizer_folders'] = lambda effect: self.clean_arcade_organizer_folders(ui)
        effects['calculate_names_char_code_warning'] = lambda effect: self.calculate_names_char_code_warning(ui)

    def calculate_file_exists(self, ui, effect) -> None:
        ui.set_value('file_exists', 'true' if self._file_system.is_file(effect['target']) else 'false')

    def remove_file(self, ui, effect) -> None:
        ui.set_value('file_exists', self._file_system.unlink(effect['target']))

    def calculate_patrons(self, ui) -> None:
        is_test_firmware, firmware_md5 = self._is_test_firmware()
        if firmware_md5 is not None:
            self._original_firmware = firmware_md5

        valid_patronkey = self._is_patronkey_valid()
        ui.set_value('can_access_patron_menu', 'true' if valid_patronkey else 'false')

        self._set_spinner_options(ui)

    def _is_patronkey_valid(self):
        if not self._file_system.is_file(UPDATE_ALL_PATREON_KEY_PATH):
            return False

        file_size = os.path.getsize(self._file_system.download_target_path(UPDATE_ALL_PATREON_KEY_PATH))
        if file_size != UPDATE_ALL_PATREON_KEY_SIZE:
            return False

        file_md5 = hashlib.md5(self._file_system.read_file_binary(UPDATE_ALL_PATREON_KEY_PATH)).hexdigest()
        if file_md5 != UPDATE_ALL_PATREON_KEY_MD5Q0:
            return False

        return True

    def _is_test_firmware(self):
        is_test_firmware, firmware_md5 = False, None
        if self._file_system.is_file(FILE_MiSTer):
            firmware_md5 = hashlib.md5(self._file_system.read_file_binary(FILE_MiSTer)).hexdigest()
            is_test_firmware = firmware_md5 == TEST_UNSTABLE_SPINNER_FIRMWARE_MD5

        return is_test_firmware, firmware_md5

    def test_unstable_spinner(self, ui) -> None:
        is_test_firmware, firmware_md5 = self._is_test_firmware()
        if is_test_firmware:
            content = self._os_utils.download(
                "https://raw.githubusercontent.com/MiSTer-devel/Distribution_MiSTer/main/MiSTer")
            self._file_system.write_file_bytes(FILE_MiSTer, content)
        else:
            content = self._os_utils.download(
                "https://raw.githubusercontent.com/theypsilon/Main_MiSTer/test-unstable-taito-spinner-firmware/bin")
            self._file_system.write_file_bytes(FILE_MiSTer, content)

        self._set_spinner_options(ui)

    def _set_spinner_options(self, ui):
        is_test_firmware, firmware_md5 = self._is_test_firmware()

        ui.set_value('test_unstable_spinner_option',
                     "Test Unstable Spinner Firmware" if not is_test_firmware else "Revert Unstable Spinner Firmware")
        ui.set_value('test_unstable_spinner_desc',
                     "For the Taito EGRET II Mini" if not is_test_firmware else "Restore the original MiSTer binary")
        ui.set_value('spinner_needs_reboot', 'true' if self._original_firmware != firmware_md5 else 'false')

    def play_bad_apple(self, _ui) -> None:
        content = self._os_utils.download(DOWNLOADER_URL)
        temp_file = self._file_system.temp_file_by_id('downloader.sh')
        self._file_system.write_file_bytes(temp_file.name, content)

        mister_ini = self._read_mister_ini()

        bad_apple_db_url = "https://github.com/theypsilon/BadAppleDB_MiSTer/releases/download/v1/bad_apple_full_res_db.json.zip"
        if 'fb_size=2' in mister_ini or 'fb_terminal=0' in mister_ini:
            bad_apple_db_url = "https://github.com/theypsilon/BadAppleDB_MiSTer/releases/download/v1/bad_apple_half_res_db.json.zip"

        env = {
            'DOWNLOADER_INI_PATH': "/tmp/downloader_bad_apple.ini",
            'ALLOW_REBOOT': '0',
            'CURL_SSL': self._config_provider.get().curl_ssl,
            'UPDATE_LINUX': 'false',
            'DEFAULT_DB_ID': 'bad_apple_db',
            'DEFAULT_DB_URL': bad_apple_db_url,
            'LOGFILE': "/tmp/downloader_bad_apple.log",
        }

        curses.endwin()

        self._os_utils.execute_process(temp_file.name, env)

        curses.initscr()

    def calculate_needs_save(self, ui) -> None:
        arcade_organizer_ini = load_ini_config_with_no_section(
            self._logger,
            Path(self._file_system.download_target_path(ARCADE_ORGANIZER_INI))
        )

        ao_variables = list_variables_with_group(settings_screen_model(), "ao_ini")
        variable_defaults = gather_default_values(settings_screen_model())

        needs_save_file_list = set()

        temp_config = Config()
        self._copy_temp_save_to_config(ui, temp_config)
        if self._downloader_ini_repository.needs_save(temp_config):
            needs_save_file_list.add("downloader.ini")

        for variable, rename in ao_variables.items():
            old_value = arcade_organizer_ini.get_string(rename, str(variable_defaults[variable])).lower()
            new_value = ui.get_value(variable)
            if old_value != new_value:
                needs_save_file_list.add("update_arcade-organizer.ini")

        config = self._config_provider.get()
        for variable in list_variables_with_group(settings_screen_model(), 'main_ini'):
            old_value = str(getattr(config, variable)).lower()
            new_value = ui.get_value(variable)
            if old_value != new_value:
                needs_save_file_list.add("update_all.ini")

        ui.set_value('needs_save', str(len(needs_save_file_list) > 0).lower())
        ui.set_value('needs_save_file_list', ", ".join(sorted(needs_save_file_list)))

    def save(self, ui) -> None:
        self.copy_ui_options_to_current_config(ui)

        variable_defaults = gather_default_values(settings_screen_model())
        main_non_default_options = self._calculate_non_default_options(ui, "main_ini", variable_defaults)
        ao_non_default_options = self._calculate_non_default_options(ui, "ao_ini", variable_defaults)

        self._write_ini_options(main_non_default_options, FILE_update_all_ini)
        self._write_ini_options(ao_non_default_options, ARCADE_ORGANIZER_INI)
        self._downloader_ini_repository.write_downloader_ini(self._config_provider.get())

    def _calculate_non_default_options(self, ui, group, variable_defaults):
        non_default_options = {}
        for variable, name in list_variables_with_group(settings_screen_model(), group).items():
            value = ui.get_value(variable)
            if value != str(variable_defaults[variable]).lower():
                non_default_options[name] = value

        return non_default_options

    def _write_ini_options(self, options, filename):
        path = Path(f'{self._config_provider.get().base_path}/{filename}')
        if len(options) == 0:
            if path.exists():
                path.unlink(missing_ok=True)
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as arcade_organizer:
            arcade_organizer.writelines(
                [f'{variable.upper()}={str(value).lower()}\n' for variable, value in options.items()])

    def copy_ui_options_to_current_config(self, ui) -> None:
        self._copy_temp_save_to_config(ui, self._config_provider.get())

    def _copy_temp_save_to_config(self, ui, config: Config) -> None:
        for variable in self._all_config_variables:
            value = dynamic_convert_string(ui.get_value(variable))
            if not isinstance(value, type(getattr(config, variable))):
                raise TypeError(f'{variable} can not have value {value}! (wrong type)')
            setattr(config, variable, value)

    @cached_property
    def _all_config_variables(self):
        return [*list_variables_with_group(settings_screen_model(), "main_ini"), *list_variables_with_group(settings_screen_model(), "downloader_only")]

    def calculate_names_char_code_warning(self, ui) -> None:

        names_char_code = ui.get_value('names_char_code').lower()

        mister_ini = self._read_mister_ini()

        has_date_code_1 = False
        if 'rbf_hide_datecode=1' in mister_ini:
            has_date_code_1 = True

        ui.set_value('names_char_code_warning',
                     'true' if names_char_code == 'char28' and not has_date_code_1 else 'false')

    def _read_mister_ini(self):
        if self._file_system.is_file(FILE_MiSTer_ini):
            return self._file_system.read_file_contents(FILE_MiSTer_ini).replace(" ", "")
        else:
            return ''

    def calculate_arcade_organizer_folders(self, ui) -> None:
        content = self._os_utils.download(ARCADE_ORGANIZER_URL)
        temp_file = self._file_system.temp_file_by_id('arcade_organizer.sh')
        self._file_system.write_file_bytes(temp_file.name, content)

        return_code, output = self._os_utils.read_command_output(['python3', temp_file.name, '--print-orgdir-folders'],
                                                                 {
                                                                     'SSL_SECURITY_OPTION': self._config_provider.get().curl_ssl,
                                                                     'INI_FILE': f'{self._config_provider.get().base_path}/{ARCADE_ORGANIZER_INI}'
                                                                 })

        ui.set_value('has_arcade_organizer_folders',
                     'true' if return_code == 0 and len(output.strip()) > 0 else 'false')
        ui.set_value('arcade_organizer_folders_list', output if return_code == 0 else '')

    def clean_arcade_organizer_folders(self, ui) -> None:
        for line in ui.get_value('arcade_organizer_folders_list').splitlines():
            self._file_system.remove_non_empty_folder(line.strip())

        ui.set_value('has_arcade_organizer_folders', 'false')
        ui.set_value('arcade_organizer_folders_list', '')
