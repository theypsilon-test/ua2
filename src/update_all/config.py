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


@dataclass
class UpdateAllIni:
    main_updater: bool = True
    encc_forks: bool = False
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


@dataclass
class UpdateJtCoresIni:
    download_beta_cores: bool = False


@dataclass
class UpdateNamesTxtIni:
    names_region: str = 'JP'
    names_char_code: str = 'CHAR18'
    names_sort_code: str = 'Common'


@dataclass
class UpdateArcadeOrganizerIni:
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


def _parse_class_field_name_from_format_equal_str(format_equal_str):
    begin = None
    for index, char in enumerate(format_equal_str):
        if char == '.':
            begin = index + 1
        elif char == '=':
            return format_equal_str[begin:index]

    raise ValueError('Not found begin or enc from: ' + format_equal_str)


K_MAIN_UPDATER = _parse_class_field_name_from_format_equal_str(f'{Config.main_updater=}')
K_JOTEGO_UPDATER = _parse_class_field_name_from_format_equal_str(f'{Config.jotego_updater=}')
K_UNOFFICIAL_UPDATER = _parse_class_field_name_from_format_equal_str(f'{Config.unofficial_updater=}')
K_LLAPI_UPDATER = _parse_class_field_name_from_format_equal_str(f'{Config.llapi_updater=}')
K_ARCADE_OFFSET_DOWNLOADER = _parse_class_field_name_from_format_equal_str(f'{Config.arcade_offset_downloader=}')
K_COIN_OP_COLLECTION_DOWNLOADER = _parse_class_field_name_from_format_equal_str(f'{Config.coin_op_collection_downloader=}')
K_ARCADE_ROMS_DB_DOWNLOADER = _parse_class_field_name_from_format_equal_str(f'{Config.arcade_roms_db_downloader=}')
K_TTY2OLED_FILES_DOWNLOADER = _parse_class_field_name_from_format_equal_str(f'{Config.tty2oled_files_downloader=}')
K_I2C2OLED_FILES_DOWNLOADER = _parse_class_field_name_from_format_equal_str(f'{Config.i2c2oled_files_downloader=}')
K_MISTERSAM_FILES_DOWNLOADER = _parse_class_field_name_from_format_equal_str(f'{Config.mistersam_files_downloader=}')
K_BIOS_GETTER = _parse_class_field_name_from_format_equal_str(f'{Config.bios_getter=}')
K_NAMES_TXT_UPDATER = _parse_class_field_name_from_format_equal_str(f'{Config.names_txt_updater=}')
