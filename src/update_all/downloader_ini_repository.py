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
import io
import json
import re
from pathlib import Path
from typing import Optional

from update_all.config import Config
from update_all.config_reader import load_ini_config_with_no_section
from update_all.constants import DOWNLOADER_INI_STANDARD_PATH, FILE_update_all_ini, FILE_update_jtcores_ini, \
    FILE_update_names_txt_ini, ARCADE_ORGANIZER_INI, FILE_update_names_txt_sh, FILE_update_jtcores_sh
from update_all.databases import candidate_databases, active_databases
from update_all.file_system import FileSystem
from update_all.logger import Logger
from update_all.os_utils import OsUtils
from update_all.settings_screen_model import settings_screen_model
from update_all.ui_model_utilities import gather_variable_descriptions, list_variables_with_group, dynamic_convert_string


default_arcade_organizer_enabled = Config().arcade_organizer


class DownloaderIniRepository:

    def __init__(self, logger: Logger, file_system: FileSystem, os_utils: OsUtils):
        self._logger = logger
        self._file_system = file_system
        self._os_utils = os_utils

    def transition_from_update_all_1(self, config: Config):
        update_all_ini_exists = self._file_system.is_file(FILE_update_all_ini)
        changes = []

        if self._file_system.is_file(DOWNLOADER_INI_STANDARD_PATH):
            if update_all_ini_exists:
                self._fill_arcade_organizer_enabled_config_field_from_update_all_ini(config)
        else:
            variable_descriptions = gather_variable_descriptions(settings_screen_model())
            if update_all_ini_exists:
                self._fill_config_with_update_all_ini(config, variable_descriptions)

            for ini_file, ini_group in [(FILE_update_jtcores_ini, "jt_ini"), (FILE_update_names_txt_ini, "names_ini")]:
                if self._file_system.is_file(ini_file):
                    self._fill_config_with_ini_file(config, ini_file, ini_group, variable_descriptions)

            self.write_downloader_ini(config)
            changes.append('A new file "downloader.ini" has been created.')

        if config.arcade_organizer != default_arcade_organizer_enabled:
            self.write_arcade_organizer_active_at_arcade_organizer_ini(config)
            changes.append(f'File "{ARCADE_ORGANIZER_INI}" now includes variable "ARCADE_ORGANIZER" previously found in "{FILE_update_all_ini}". It indicates whether the Arcade Organizer is enabled in Update All.')

        for file in [FILE_update_all_ini, FILE_update_jtcores_ini, FILE_update_names_txt_ini, FILE_update_jtcores_sh, FILE_update_names_txt_sh]:
            if self._file_system.is_file(file):
                self._file_system.unlink(file, verbose=False)
                changes.append(f'File "{file}" removed.')

        if len(changes) >= 1:
            coming_from_update_all_1 = len(changes) >= 2 or 'downloader.ini' not in changes[0]
            if coming_from_update_all_1:
                self._logger.print('Transitioning from Update All 1:')
            else:
                self._logger.print('Setting default options:')

            for change in changes:
                self._logger.print(f'  - {change}')
            self._logger.print()
            if coming_from_update_all_1:
                self._logger.print('Waiting 10 seconds...')
                self._os_utils.sleep(10.0)

    def _fill_arcade_organizer_enabled_config_field_from_update_all_ini(self, config):
        ini_content = load_ini_config_with_no_section(self._logger, self._file_system, FILE_update_all_ini)
        config.arcade_organizer = ini_content.get_bool('arcade_organizer', default_arcade_organizer_enabled)

    def _fill_config_with_update_all_ini(self, config, variable_descriptions):
        update_all_ini = self._fill_config_with_ini_file(config, FILE_update_all_ini, "ua_ini", variable_descriptions)
        config.arcade_roms_db_downloader = config.arcade_roms_db_downloader or \
                                           update_all_ini.get_bool('mame_getter', False) or \
                                           update_all_ini.get_bool('hbmame_getter', False)

    def _fill_config_with_ini_file(self, config, ini_file, ini_group, variable_descriptions):
        ini_content = load_ini_config_with_no_section(self._logger, self._file_system, ini_file)

        for variable in list_variables_with_group(settings_screen_model(), ini_group):
            string_value = ini_content.get_string(variable, None)
            if string_value is None:
                setattr(config, variable, dynamic_convert_string(variable_descriptions[variable]['default']))
            else:
                string_value = self._ensure_string_value_is_possible(string_value, variable_descriptions[variable]['values'])

                setattr(config, variable, dynamic_convert_string(string_value))

        return ini_content

    @staticmethod
    def _ensure_string_value_is_possible(string_value, possible_values):
        if string_value in possible_values:
            return string_value

        for pb in possible_values:
            if pb.lower() == string_value.lower():
                return string_value

        raise ValueError(f'Value {string_value} is not among the possible values: {", ".join(possible_values)}')

    def needs_save(self, config: Config) -> bool:
        if not self._file_system.is_file(DOWNLOADER_INI_STANDARD_PATH):
            ini = {}
            self._add_new_downloader_ini_changes(ini, config)
            return len(ini) > 0

        new_ini_contents = self._build_new_downloader_ini_contents(config)
        if new_ini_contents is None:
            return False
        new_ini_contents = new_ini_contents.strip().lower()

        current_ini_contents = self._file_system.read_file_contents(DOWNLOADER_INI_STANDARD_PATH).strip().lower()
        return new_ini_contents != current_ini_contents

    def write_arcade_organizer_active_at_arcade_organizer_ini(self, config):
        contents = ''
        if self._file_system.is_file(ARCADE_ORGANIZER_INI):
            contents = self._file_system.read_file_contents(ARCADE_ORGANIZER_INI).strip()
            if 'arcade_organizer' in contents.lower():
                return
            contents += '\n'

        contents += f'ARCADE_ORGANIZER={str(config.arcade_organizer).lower()}\n'
        contents += '\n'

        self._file_system.write_file_contents(ARCADE_ORGANIZER_INI, contents)

    def write_downloader_ini(self, config: Config, target_path: str = None) -> None:
        new_ini_contents = self._build_new_downloader_ini_contents(config)
        if new_ini_contents is not None:
            self._file_system.write_file_contents(target_path or DOWNLOADER_INI_STANDARD_PATH, new_ini_contents)

    def _internal_read_downloader_ini(self):
        ini_contents = ''
        try:
            ini_contents = self._file_system.read_file_contents(DOWNLOADER_INI_STANDARD_PATH)
            parser = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
            parser.read_string(ini_contents)
            return {header.lower(): {k.lower(): v for k, v in section.items()} for header, section in parser.items() if
                   header.lower() != 'default'}
        except Exception as e:
            self._logger.debug(f'Could not read ini file {DOWNLOADER_INI_STANDARD_PATH}')
            self._logger.debug(e)
            self._logger.debug(f'ini_contents: {ini_contents}')
            return {}

    def _add_new_downloader_ini_changes(self, ini, config: Config):
        for _, db in candidate_databases(config):
            db_id = db.db_id.lower()
            if db in active_databases(config):
                if db_id not in ini:
                    ini[db_id] = {}
                ini[db_id]['db_url'] = db.db_url
            elif db_id in ini:
                del ini[db_id]

    def _build_new_downloader_ini_contents(self, config: Config) -> Optional[str]:
        ini: dict[str, dict[str, str]] = self._internal_read_downloader_ini()
        before = json.dumps(ini)
        self._add_new_downloader_ini_changes(ini, config)
        after = json.dumps(ini)

        if before == after:
            return None

        db_ids = {db.db_id.lower(): db.db_id for _, db in candidate_databases(config)}

        mister_section = ''
        nomister_section = ''
        pre_section = ''

        if self._file_system.is_file(DOWNLOADER_INI_STANDARD_PATH):
            header_regex = re.compile('\s*\[([-_/a-zA-Z0-9]+)\].*', re.I)
            ini_contents = io.StringIO(self._file_system.read_file_contents(DOWNLOADER_INI_STANDARD_PATH))

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

                    if section.lower() == 'mister':
                        mister_section += line
                    else:
                        nomister_section += line
                else:
                    raise Exception("Wrong state: " + str(state))

        parser = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        for header, section_id in ini.items():
            if header in db_ids:
                header = db_ids[header]
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
            return ss.read()
