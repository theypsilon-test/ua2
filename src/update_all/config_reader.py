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
from typing import List, Tuple

from update_all.config import Config
from update_all.constants import MEDIA_FAT, KENV_CURL_SSL, KENV_COMMIT, KENV_LOCATION_STR, \
    DOWNLOADER_INI_STANDARD_PATH, ARCADE_ORGANIZER_INI,MISTER_ENVIRONMENT, KENV_DEBUG
from update_all.databases import DB_ID_JTCORES, DB_ID_NAMES_TXT, names_locale_by_db_url, model_variables_by_db_id, \
    Database, db_distribution_mister_by_encc_forks, db_jtcores_by_download_beta_cores, db_names_txt_by_locale, \
    dbs_to_model_variables_pairs, AllDBs
from update_all.file_system import FileSystem
from update_all.ini_parser import IniParser
from update_all.local_store import LocalStore
from update_all.logger import Logger


class ConfigReader:
    def __init__(self, logger: Logger, env: dict[str, str]):
        self._logger = logger
        self._env = env
        self._downloader_ini = {}

    def fill_config_with_environment_and_mister_section(self, config: Config):
        self._initialize_downloader_ini()
        if 'mister' in self._downloader_ini:
            mister_section = self._downloader_ini['mister']
            config.base_path = mister_section.get_string('base_path', config.base_path)
            config.base_system_path = mister_section.get_string('base_system_path', config.base_path)
            config.paths_from_downloader_ini = mister_section.has('base_path')
            config.verbose = mister_section.get_bool('verbose', False)
        else:
            config.base_path = str(calculate_base_path(self._env))
            config.base_system_path = config.base_path

        if is_debug_enabled(self._env):
            config.verbose = True

        config.curl_ssl = valid_max_length(KENV_CURL_SSL, self._env[KENV_CURL_SSL], 50)
        config.commit = valid_max_length(KENV_COMMIT, self._env[KENV_COMMIT], 50)
        config.start_time = time.time()

        self._logger.configure(config)

        if not is_mister_environment(self._env):
            config.not_mister = True

        self._logger.debug('env: ' + json.dumps(self._env, indent=4))

    def fill_config_with_ini_files(self, config: Config, file_system: FileSystem) -> None:
        self._initialize_downloader_ini()

        for db_id, variable in model_variables_by_db_id().items():
            is_present = db_id.lower() in self._downloader_ini
            config.__setattr__(variable, is_present)
            if is_present:
                config.databases.add(db_id)

        if DB_ID_JTCORES in self._downloader_ini:
            config.download_beta_cores = self._downloader_ini[DB_ID_JTCORES].get_string('db_url', AllDBs.JTSTABLE_JTCORES.db_url) == 'https://raw.githubusercontent.com/jotego/jtpremium/main/jtbindb.json.zip'

        if DB_ID_NAMES_TXT in self._downloader_ini:
            config.names_region, config.names_char_code, config.names_sort_code = names_locale_by_db_url(self._downloader_ini[DB_ID_NAMES_TXT].get_string('db_url', AllDBs.NAMES_CHAR18_COMMON_JP_TXT.db_url))

        if AllDBs.ARCADE_ROMS.db_id in self._downloader_ini and 'filter' in self._downloader_ini[AllDBs.ARCADE_ROMS.db_id]:
            config.hbmame_filter = '!hbmame' in self._downloader_ini[AllDBs.ARCADE_ROMS.db_id].get_string('filter', '')

        arcade_organizer_ini = load_ini_config_with_no_section(self._logger, file_system, ARCADE_ORGANIZER_INI)
        config.arcade_organizer = arcade_organizer_ini.get_bool('arcade_organizer', config.arcade_organizer)

        self._logger.debug('config: ' + json.dumps(config, default=lambda o: str(o) if isinstance(o, Path) or isinstance(o, set) else o.__dict__, indent=4))

    def fill_config_with_local_store(self, config: Config, store: LocalStore):
        config.wait_time_for_reading = store.get_wait_time_for_reading()
        config.countdown_time = store.get_countdown_time()
        config.autoreboot = store.get_autoreboot()

    def _initialize_downloader_ini(self):
        if len(self._downloader_ini) > 0:
            """It should be initialized only once"""
            return

        downloader_ini = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
        try:
            downloader_ini.read_string(Path(f'{str(calculate_base_path(self._env))}/{DOWNLOADER_INI_STANDARD_PATH}').read_text())
        except Exception as _:
            return

        self._downloader_ini = {section.lower(): IniParser(downloader_ini[section]) for section in downloader_ini.sections()}


def valid_max_length( key: str, value: str, max_limit: int) -> str:
    if len(value) <= max_limit:
        return value

    raise InvalidConfigParameter(f"Invalid {key} with value '{value}'. Too long string (max is {max_limit}).")


def candidate_databases(config: Config) -> List[Tuple[str, Database]]:
    configurable_dbs = {
        'main_updater': db_distribution_mister_by_encc_forks(config.encc_forks),
        'jotego_updater': db_jtcores_by_download_beta_cores(config.download_beta_cores),
        'names_txt_updater': db_names_txt_by_locale(config.names_region, config.names_char_code, config.names_sort_code)
    }
    result = []
    for variable, dbs in dbs_to_model_variables_pairs():
        if variable in configurable_dbs:
            result.append((variable, configurable_dbs[variable]))
            continue

        if len(dbs) != 1:
            raise ValueError(f"Needs to be length 1, but is '{len(dbs)}', or must be contained in configurable_dbs.")

        result.append((variable, dbs[0]))
    return result


def active_databases(config: Config) -> list[Database]:
    return [db for var, db in candidate_databases(config) if db.db_id in config.databases]


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


