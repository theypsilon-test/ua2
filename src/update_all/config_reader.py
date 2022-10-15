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
import json
import time
from distutils.util import strtobool
from enum import unique, IntEnum
from pathlib import Path
from typing import Tuple

from update_all.config import Config
from update_all.constants import MEDIA_FAT, KENV_CURL_SSL, KENV_COMMIT, KENV_LOCATION_STR, \
    DOWNLOADER_INI_STANDARD_PATH, FILE_update_all_ini, ARCADE_ORGANIZER_INI,MISTER_ENVIRONMENT, KENV_DEBUG
from update_all.databases import DB_ID_JTCORES, DB_ID_NAMES_TXT, names_locale_by_db_url
from update_all.ini_parser import IniParser
from update_all.logger import Logger
from update_all.settings_screen_model import settings_screen_model
from update_all.ui_model_utilities import gather_default_values, list_variables_with_group, dynamic_convert_string


@unique
class AllowDelete(IntEnum):
    NONE = 0
    ALL = 1
    OLD_RBF = 2


class ConfigProvider:
    _config: Config

    def __init__(self):
        self._config = None

    def initialize(self, config: Config) -> None:
        assert(self._config is None)
        self._config = config

    def get(self) -> Config:
        assert(self._config is not None)
        return self._config


class ConfigReader:
    def __init__(self, logger: Logger, env: dict[str, str]):
        self._logger = logger
        self._env = env

    def read_config(self) -> Tuple[Config, bool]:
        result = Config()
        result.base_path = str(calculate_base_path(self._env))

        if is_debug_enabled(self._env):
            result.verbose = True

        downloader_ini_path = Path(f'{result.base_path}/{DOWNLOADER_INI_STANDARD_PATH}')
        update_all_ini_path = Path(f'{result.base_path}/{FILE_update_all_ini}')
        arcade_organizer_ini_path = Path(f'{result.base_path}/{ARCADE_ORGANIZER_INI}')

        is_file_read = downloader_ini_path.exists() or update_all_ini_path.exists() or arcade_organizer_ini_path.exists()

        downloader_ini = None
        downloader_sections = set()
        if downloader_ini_path.exists():
            downloader_ini = self._load_ini_config_from_file(str(downloader_ini_path))
            downloader_sections = set([section.lower() for section in downloader_ini.sections()])

        update_all_ini = load_ini_config_with_no_section(self._logger, update_all_ini_path)

        ini_default_values = gather_default_values(settings_screen_model())
        for variable in list_variables_with_group(settings_screen_model(), "ua_ini"):
            string_value = update_all_ini.get_string(variable, str(ini_default_values[variable]).lower())
            setattr(result, variable, dynamic_convert_string(string_value))

        result.arcade_roms_db_downloader = result.arcade_roms_db_downloader or update_all_ini.get_bool('mame_getter', False) or update_all_ini.get_bool('hbmame_getter', False)

        if DB_ID_JTCORES in downloader_sections:
            result.download_beta_cores = downloader_ini[DB_ID_JTCORES]['db_url'] == 'https://raw.githubusercontent.com/jotego/jtpremium/main/jtbindb.json.zip'

        if DB_ID_NAMES_TXT in downloader_sections:
            result.names_region, result.names_char_code, result.names_sort_code = names_locale_by_db_url(downloader_ini[DB_ID_NAMES_TXT]['db_url'])

        result.curl_ssl = self._valid_max_length(KENV_CURL_SSL, self._env[KENV_CURL_SSL], 50)
        result.commit = self._valid_max_length(KENV_COMMIT, self._env[KENV_COMMIT], 50)
        result.start_time = time.time()

        self._logger.configure(result)

        if not is_mister_environment(self._env):
            result.not_mister = True

        self._logger.debug('env: ' + json.dumps(self._env, indent=4))
        self._logger.debug('config: ' + json.dumps(result, default=lambda o: str(o) if isinstance(o, Path) else o.__dict__, indent=4))

        return result, is_file_read

    def _load_ini_config_from_file(self, config_path):
        ini_config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        try:
            ini_config.read(config_path)
        except Exception as e:
            self._logger.debug(e)
            self._logger.print('Could not read ini file %s' % config_path)
            raise e
        return ini_config

    def _valid_max_length(self, key: str, value: str, max_limit: int) -> str:
        if len(value) <= max_limit:
            return value

        raise InvalidConfigParameter(f"Invalid {key} with value '{value}'. Too long string (max is {max_limit}).")


def load_ini_config_with_no_section(logger: Logger, config_path: Path):
    if not config_path.exists():
        return IniParser({})

    ini_config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
    content = f'[default]\n{config_path.read_text().lower()}'
    try:
        ini_config.read_string(content)
    except Exception as e:
        logger.debug(e)
        logger.print('Incorrect format for ini file: %s' % str(config_path))
        return IniParser({})

    return IniParser(ini_config['default'])


def calculate_base_path(env):
    if is_mister_environment(env):
        return Path(MEDIA_FAT)
    else:
        return Path(env[KENV_LOCATION_STR]).resolve()


def is_mister_environment(env):
    return env[KENV_LOCATION_STR].strip().lower() == MISTER_ENVIRONMENT


def is_debug_enabled(env):
    return strtobool(env[KENV_DEBUG].strip().lower())


class InvalidConfigParameter(Exception):
    pass


