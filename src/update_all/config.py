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
import json
import time
from dataclasses import dataclass
from enum import unique, IntEnum
from pathlib import Path
from typing import Tuple

from update_all.constants import KENV_INI_PATH, MEDIA_FAT, KENV_CURL_SSL, KENV_COMMIT, DEFAULT_CURL_SSL_OPTIONS, \
    DEFAULT_COMMIT, DEFAULT_INI_PATH
from update_all.logger import Logger


@unique
class AllowDelete(IntEnum):
    NONE = 0
    ALL = 1
    OLD_RBF = 2


@dataclass
class Config:
    # Not really a config
    start_time: float = 0.0

    # From the environment
    curl_ssl: str = DEFAULT_CURL_SSL_OPTIONS
    commit: str = DEFAULT_COMMIT
    ini_path: Path = Path(DEFAULT_INI_PATH)

    # General options
    base_path: str = MEDIA_FAT
    allow_reboot: bool = True
    update_linux: bool = True
    verbose: bool = False
    debug: bool = False

    # Global Updating Toggles
    main_updater: bool = True
    jotego_updater: bool = True
    unofficial_updater: bool = False
    llapi_updater: bool = False
    arcade_offset_downloader: bool = False
    arcade_roms_db_downloader: bool = False
    tty2oled_files_downloader: bool = False
    i2c2oled_files_downloader: bool = False
    mistersam_files_downloader: bool = False
    bios_getter: bool = False
    mame_getter: bool = False
    hbmame_getter: bool = False
    names_txt_updater: bool = True
    arcade_organizer: bool = True

    # Specific Updating Toggles
    encc_forks: bool = False
    download_beta_cores: bool = False
    names_region: str = 'JP'
    names_char_code: str = 'CHAR18'
    names_sort_code: str = 'Common'

    # Misc Options
    wait_time_for_reading: int = 4


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

    @property
    def ini_path(self) -> str:
        return self._env[KENV_INI_PATH]

    def read_config(self) -> Tuple[Config, bool]:
        result = Config()
        is_file_read = False

        result.base_path = str(Path(self.ini_path).resolve().parent.parent)
        result.curl_ssl = self._valid_max_length(KENV_CURL_SSL, self._env[KENV_CURL_SSL], 50)
        result.commit = self._valid_max_length(KENV_COMMIT, self._env[KENV_COMMIT], 50)
        result.start_time = time.time()

        self._logger.configure(result)

        self._logger.debug('env: ' + json.dumps(self._env, indent=4))
        self._logger.debug('config: ' + json.dumps(result, default=lambda o: str(o) if isinstance(o, Path) else o.__dict__, indent=4))

        result.ini_path = Path(self.ini_path)

        return result, is_file_read

    def _valid_max_length(self, key: str, value: str, max_limit: int) -> str:
        if len(value) <= max_limit:
            return value

        raise InvalidConfigParameter(f"Invalid {key} with value '{value}'. Too long string (max is {max_limit}).")


class InvalidConfigParameter(Exception):
    pass


