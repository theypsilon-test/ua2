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
from dataclasses import dataclass
from enum import unique, IntEnum

from update_all.constants import DEFAULT_CURL_SSL_OPTIONS, DEFAULT_COMMIT, MEDIA_FAT


@dataclass
class Config:
    # Not really a config
    start_time: float = 0.0

    # From the environment
    curl_ssl: str = DEFAULT_CURL_SSL_OPTIONS
    commit: str = DEFAULT_COMMIT

    # General options
    base_path: str = MEDIA_FAT
    autoreboot: bool = True
    update_linux: bool = True
    not_mister: bool = False
    verbose: bool = False
    temporary_downloader_ini: bool = False

    # Global Updating Toggles
    main_updater: bool = True
    jotego_updater: bool = True
    unofficial_updater: bool = False
    llapi_updater: bool = False
    arcade_offset_downloader: bool = False
    coin_op_collection_downloader: bool = True
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
    wait_time_for_reading: int = 2
    countdown_time: int = 15


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
        if self._config is not None:
            raise Exception("Config must be initialized only once.")
        self._config = config

    def get(self) -> Config:
        if self._config is None:
            raise Exception("Config must be initialized before calling this method.")
        return self._config
