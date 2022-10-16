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
from pathlib import Path

from update_all.config import Config
from update_all.constants import MEDIA_FAT, KENV_CURL_SSL, KENV_COMMIT, KENV_LOCATION_STR, \
    DOWNLOADER_INI_STANDARD_PATH, ARCADE_ORGANIZER_INI,MISTER_ENVIRONMENT, KENV_DEBUG
from update_all.databases import DB_ID_JTCORES, DB_ID_NAMES_TXT, names_locale_by_db_url, config_fields_by_db_id
from update_all.file_system import FileSystem
from update_all.ini_parser import IniParser
from update_all.logger import Logger


class ConfigReader:
    def __init__(self, logger: Logger, env: dict[str, str]):
        self._logger = logger
        self._env = env

    def fill_config_with_environment(self, config: Config) -> None:
        config.base_path = str(calculate_base_path(self._env))

        if is_debug_enabled(self._env):
            config.verbose = True

        config.curl_ssl = self._valid_max_length(KENV_CURL_SSL, self._env[KENV_CURL_SSL], 50)
        config.commit = self._valid_max_length(KENV_COMMIT, self._env[KENV_COMMIT], 50)
        config.start_time = time.time()

        self._logger.configure(config)

        if not is_mister_environment(self._env):
            config.not_mister = True

        self._logger.debug('env: ' + json.dumps(self._env, indent=4))

    def fill_config_with_ini_files(self, config: Config, file_system: FileSystem) -> None:
        downloader_ini = None
        downloader_sections = set()
        if file_system.is_file(DOWNLOADER_INI_STANDARD_PATH):
            downloader_ini = self._load_ini_config_from_contents(file_system.read_file_contents(DOWNLOADER_INI_STANDARD_PATH))
            downloader_sections = set([section.lower() for section in downloader_ini.sections()])

        for db_id, config_field in config_fields_by_db_id().items():
            is_present = db_id.lower() in downloader_sections
            config.__setattr__(config_field, is_present)

        if DB_ID_JTCORES in downloader_sections:
            config.download_beta_cores = downloader_ini[DB_ID_JTCORES]['db_url'] == 'https://raw.githubusercontent.com/jotego/jtpremium/main/jtbindb.json.zip'

        if DB_ID_NAMES_TXT in downloader_sections:
            config.names_region, config.names_char_code, config.names_sort_code = names_locale_by_db_url(downloader_ini[DB_ID_NAMES_TXT]['db_url'])

        arcade_organizer_ini = load_ini_config_with_no_section(self._logger, file_system, ARCADE_ORGANIZER_INI)
        config.arcade_organizer = arcade_organizer_ini.get_bool('arcade_organizer', config.arcade_organizer)

        self._logger.debug('config: ' + json.dumps(config, default=lambda o: str(o) if isinstance(o, Path) else o.__dict__, indent=4))

    def _load_ini_config_from_contents(self, contents):
        ini_config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        try:
            ini_config.read_string(contents)
        except Exception as e:
            self._logger.debug('Could not read ini file: %s' % contents)
            self._logger.debug(e)
            raise e
        return ini_config

    def _valid_max_length(self, key: str, value: str, max_limit: int) -> str:
        if len(value) <= max_limit:
            return value

        raise InvalidConfigParameter(f"Invalid {key} with value '{value}'. Too long string (max is {max_limit}).")


def load_ini_config_with_no_section(logger: Logger, file_system: FileSystem, path: str):
    if not file_system.is_file(path):
        return IniParser({})

    ini_config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
    content = f'[default]\n{file_system.read_file_contents(path).lower()}'
    try:
        ini_config.read_string(content)
    except Exception as e:
        logger.debug('Incorrect format for ini file: %s' % path)
        logger.debug(e)
        logger.debug(f'content: {content}')
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


