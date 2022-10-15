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
import dataclasses
from functools import cache
from typing import Dict, List, Tuple
from update_all.config import K_MAIN_UPDATER, K_JOTEGO_UPDATER, K_UNOFFICIAL_UPDATER, K_LLAPI_UPDATER, \
    K_ARCADE_OFFSET_DOWNLOADER, K_COIN_OP_COLLECTION_DOWNLOADER, K_ARCADE_ROMS_DB_DOWNLOADER, \
    K_TTY2OLED_FILES_DOWNLOADER, K_I2C2OLED_FILES_DOWNLOADER, K_MISTERSAM_FILES_DOWNLOADER, K_BIOS_GETTER, \
    K_NAMES_TXT_UPDATER, Config


class Database:
    def __init__(self, db_id: str, db_url: str, title: str):
        self.db_id = db_id
        self.db_url = db_url
        self.title = title

DB_ID_DISTRIBUTION_MISTER = 'distribution_mister'
DB_ID_JTCORES = 'jtcores'
DB_ID_NAMES_TXT = 'names_txt'

class AllDBs:
    # Distribution MiSTer
    MISTER_DEVEL_DISTRIBUTION_MISTER = Database(db_id=DB_ID_DISTRIBUTION_MISTER, db_url='https://raw.githubusercontent.com/MiSTer-devel/Distribution_MiSTer/main/db.json.zip', title='Main Distribution: MiSTer-devel')
    MISTER_DB9_DISTRIBUTION_MISTER = Database(db_id=DB_ID_DISTRIBUTION_MISTER, db_url='https://raw.githubusercontent.com/MiSTer-DB9/Distribution_MiSTer/main/dbencc.json.zip', title='Main Distribution: DB9 / SNAC8')

    # JTCORES
    JTBIN_JTCORES = Database(db_id=DB_ID_JTCORES, db_url='https://raw.githubusercontent.com/jotego/jtpremium/main/jtbindb.json.zip', title='JTCORES for MiSTer (jtpremium)')
    JTSTABLE_JTCORES = Database(db_id=DB_ID_JTCORES, db_url='https://raw.githubusercontent.com/jotego/jtcores_mister/main/jtbindb.json.zip', title='JTCORES for MiSTer')

    # UNOFFICIAL CORES
    THEYPSILON_UNOFFICIAL_DISTRIBUTION = Database(db_id='theypsilon_unofficial_distribution', db_url='https://raw.githubusercontent.com/theypsilon/Distribution_Unofficial_MiSTer/main/unofficialdb.json.zip', title='theypsilon Unofficial Distribution')
    LLAPI_FOLDER = Database(db_id='llapi_folder', db_url='https://raw.githubusercontent.com/MiSTer-LLAPI/LLAPI_folder_MiSTer/main/llapidb.json.zip', title='LLAPI Folder')
    ARCADE_OFFSET_FOLDER = Database(db_id='arcade_offset_folder', db_url='https://raw.githubusercontent.com/atrac17/Arcade_Offset/db/arcadeoffsetdb.json.zip', title='Arcade Offset folder')
    COIN_OP_COLLECTION = Database(db_id='atrac17/Coin-Op_Collection', db_url='https://raw.githubusercontent.com/atrac17/Coin-Op_Collection/db/db.json.zip', title='Coin-Op Collection')

    # NAMES TXT
    NAMES_CHAR54_MANUFACTURER_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR54_Manufacturer_EU.json', title='Names TXT: CHAR54 Manufacturer EU')
    NAMES_CHAR28_MANUFACTURER_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Manufacturer_EU.json', title='Names TXT: CHAR28 Manufacturer EU')
    NAMES_CHAR28_MANUFACTURER_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Manufacturer_US.json', title='Names TXT: CHAR28 Manufacturer US')
    NAMES_CHAR28_MANUFACTURER_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Manufacturer_JP.json', title='Names TXT: CHAR28 Manufacturer JP')
    NAMES_CHAR28_COMMON_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Common_EU.json', title='Names TXT: CHAR28 Common EU')
    NAMES_CHAR28_COMMON_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Common_US.json', title='Names TXT: CHAR28 Common US')
    NAMES_CHAR28_COMMON_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Common_JP.json', title='Names TXT: CHAR28 Common JP')
    NAMES_CHAR18_MANUFACTURER_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Manufacturer_EU.json', title='Names TXT: CHAR18 Manufacturer EU')
    NAMES_CHAR18_MANUFACTURER_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Manufacturer_US.json', title='Names TXT: CHAR18 Manufacturer US')
    NAMES_CHAR18_MANUFACTURER_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Manufacturer_JP.json', title='Names TXT: CHAR18 Manufacturer JP')
    NAMES_CHAR18_COMMON_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Common_EU.json', title='Names TXT: CHAR18 Common EU')
    NAMES_CHAR18_COMMON_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Common_US.json', title='Names TXT: CHAR18 Common US')
    NAMES_CHAR18_COMMON_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Common_JP.json', title='Names TXT: CHAR18 Common JP')

    # UNOFFICIAL SCRIPTS
    TTY2OLED_FILES = Database(db_id='tty2oled_files', db_url='https://raw.githubusercontent.com/venice1200/MiSTer_tty2oled/main/tty2oleddb.json', title='tty2oled files')
    I2C2OLED_FILES = Database(db_id='i2c2oled_files', db_url='https://raw.githubusercontent.com/venice1200/MiSTer_i2c2oled/main/i2c2oleddb.json', title='i2c2oled files')
    MISTERSAM_FILES = Database(db_id='MiSTer_SAM_files', db_url='https://raw.githubusercontent.com/mrchrisster/MiSTer_SAM/main/MiSTer_SAMdb.json', title='MiSTer SAM files')

    # ROMS
    BIOS = Database(db_id='bios_db', db_url='https://raw.githubusercontent.com/theypsilon/BiosDB_MiSTer/db/bios_db.json', title='BIOS Database')
    ARCADE_ROMS = Database(db_id='arcade_roms_db', db_url='https://raw.githubusercontent.com/theypsilon/ArcadeROMsDB_MiSTer/db/arcade_roms_db.json.zip', title='Arcade ROMs Database')


def candidate_databases(config: Config) -> List[Tuple[str, Database]]:
    configurable_dbs = {
        K_MAIN_UPDATER: db_distribution_mister_by_encc_forks(config.encc_forks),
        K_JOTEGO_UPDATER: db_jtcores_by_download_beta_cores(config.download_beta_cores),
        K_NAMES_TXT_UPDATER: db_names_txt_by_locale(config.names_region, config.names_char_code, config.names_sort_code)
    }
    result = []
    for config_field, dbs in dbs_to_config_fields_pairs():
        if config_field in configurable_dbs:
            result.append((config_field, configurable_dbs[config_field]))
            continue

        if len(dbs) != 1:
            raise ValueError(f"Needs to be length 1, but is '{len(dbs)}', or must be contained in configurable_dbs.")

        result.append((config_field, dbs[0]))
    return result


@cache
def dbs_to_config_fields_pairs() -> List[Tuple[str, List[Database]]]:
    mapping = databases_by_ids()
    return [(config_field, mapping[db_id]) for config_field, db_id in db_ids_to_config_field_pairs() ]


@cache
def db_ids_to_config_field_pairs() -> List[Tuple[str, str]]:
    return [
        (K_MAIN_UPDATER, DB_ID_DISTRIBUTION_MISTER),
        (K_JOTEGO_UPDATER, DB_ID_JTCORES),
        (K_UNOFFICIAL_UPDATER, AllDBs.THEYPSILON_UNOFFICIAL_DISTRIBUTION.db_id),
        (K_LLAPI_UPDATER, AllDBs.LLAPI_FOLDER.db_id),
        (K_ARCADE_OFFSET_DOWNLOADER, AllDBs.ARCADE_OFFSET_FOLDER.db_id),
        (K_COIN_OP_COLLECTION_DOWNLOADER, AllDBs.COIN_OP_COLLECTION.db_id),
        (K_ARCADE_ROMS_DB_DOWNLOADER, AllDBs.ARCADE_ROMS.db_id),
        (K_TTY2OLED_FILES_DOWNLOADER, AllDBs.TTY2OLED_FILES.db_id),
        (K_I2C2OLED_FILES_DOWNLOADER, AllDBs.I2C2OLED_FILES.db_id),
        (K_MISTERSAM_FILES_DOWNLOADER, AllDBs.MISTERSAM_FILES.db_id),
        (K_BIOS_GETTER, AllDBs.BIOS.db_id),
        (K_NAMES_TXT_UPDATER, DB_ID_NAMES_TXT),
    ]


@cache
def config_field_by_db_ids() -> Dict[str, str]:
    return {db.db_id: config_field for config_field, db in candidate_databases(Config())}


def active_databases(config: Config) -> list[Database]:
    return [db for var, db in candidate_databases(config) if dataclasses.asdict(config)[var.lower()]]


@cache
def all_dbs_list() -> List[Database]:
    return [db for field_name, db in AllDBs.__dict__.items() if not field_name.startswith('_')]


@cache
def databases_by_ids() -> Dict[str, List[Database]]:
    result = {}
    for db in all_dbs_list():
        if db.db_id not in result:
            result[db.db_id] = []

        result[db.db_id].append(db)
    return result


def db_distribution_mister_by_encc_forks(encc_forks: bool) -> Database:
    return AllDBs.MISTER_DB9_DISTRIBUTION_MISTER if encc_forks else AllDBs.MISTER_DEVEL_DISTRIBUTION_MISTER


def db_jtcores_by_download_beta_cores(download_beta_cores: bool) -> Database:
    return AllDBs.JTBIN_JTCORES if download_beta_cores else AllDBs.JTSTABLE_JTCORES


def db_names_txt_by_locale(region: str, char_code: str, sort_code: str) -> Database:
    return _names_dict.get(region, {}).get(char_code, {}).get(sort_code, AllDBs.NAMES_CHAR18_COMMON_JP_TXT)


def names_locale_by_db_url(db_url) -> (str, str, str):
    for region in _names_dict:
        for char_code in _names_dict[region]:
            for sort_code, db in _names_dict[region][char_code].items():
                if db_url == db.db_url:
                    return region, char_code, sort_code

    if db_url == AllDBs.NAMES_CHAR18_COMMON_JP_TXT.db_url:
        raise ValueError('Could not find a value for DB_NAMES_CHAR18_COMMON_JP_TXT')

    return names_locale_by_db_url(AllDBs.NAMES_CHAR18_COMMON_JP_TXT.db_url)


_names_dict = {
    'JP': {
        'CHAR18': {
            'Common': AllDBs.NAMES_CHAR18_COMMON_JP_TXT,
            'Manufacturer': AllDBs.NAMES_CHAR18_MANUFACTURER_JP_TXT
        },
        'CHAR28': {
            'Common': AllDBs.NAMES_CHAR28_COMMON_JP_TXT,
            'Manufacturer': AllDBs.NAMES_CHAR28_MANUFACTURER_JP_TXT
        }
    },
    'US': {
        'CHAR18': {
            'Common': AllDBs.NAMES_CHAR18_COMMON_US_TXT,
            'Manufacturer': AllDBs.NAMES_CHAR18_MANUFACTURER_US_TXT
        },
        'CHAR28': {
            'Common': AllDBs.NAMES_CHAR28_COMMON_US_TXT,
            'Manufacturer': AllDBs.NAMES_CHAR28_MANUFACTURER_US_TXT
        }
    },
    'EU': {
        'CHAR18': {
            'Common': AllDBs.NAMES_CHAR18_COMMON_EU_TXT,
            'Manufacturer': AllDBs.NAMES_CHAR18_MANUFACTURER_EU_TXT
        },
        'CHAR28': {
            'Common': AllDBs.NAMES_CHAR28_COMMON_EU_TXT,
            'Manufacturer': AllDBs.NAMES_CHAR28_MANUFACTURER_EU_TXT
        },
        'CHAR54': {
            'Manufacturer': AllDBs.NAMES_CHAR54_MANUFACTURER_EU_TXT
        }
    }
}
