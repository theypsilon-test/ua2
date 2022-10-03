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

class Database:
    def __init__(self, db_id: str, db_url: str, title: str):
        self.db_id = db_id
        self.db_url = db_url
        self.title = title


DB_ID_DISTRIBUTION_MISTER = 'distribution_mister'
DB_MISTER_DEVEL_DISTRIBUTION_MISTER = Database(db_id=DB_ID_DISTRIBUTION_MISTER, db_url='https://raw.githubusercontent.com/MiSTer-devel/Distribution_MiSTer/main/db.json.zip', title='Main Distribution: MiSTer-devel')
DB_MISTER_DB9_DISTRIBUTION_MISTER = Database(db_id=DB_ID_DISTRIBUTION_MISTER, db_url='https://raw.githubusercontent.com/MiSTer-DB9/Distribution_MiSTer/main/dbencc.json.zip', title='Main Distribution: DB9 / SNAC8')


def db_distribution_mister_by_encc_forks(encc_forks: bool) -> Database:
    return DB_MISTER_DB9_DISTRIBUTION_MISTER if encc_forks else DB_MISTER_DEVEL_DISTRIBUTION_MISTER


DB_ID_JTCORES = 'jtcores'
DB_JTBIN_JTCORES = Database(db_id=DB_ID_JTCORES, db_url='https://raw.githubusercontent.com/jotego/jtpremium/main/jtbindb.json.zip', title='JTCORES for MiSTer (jtpremium)')
DB_JTSTABLE_JTCORES = Database(db_id=DB_ID_JTCORES, db_url='https://raw.githubusercontent.com/jotego/jtcores_mister/main/jtbindb.json.zip', title='JTCORES for MiSTer')


def db_jtcores_by_download_beta_cores(download_beta_cores: bool) -> Database:
    return DB_JTBIN_JTCORES if download_beta_cores else DB_JTSTABLE_JTCORES


DB_THEYPSILON_UNOFFICIAL_DISTRIBUTION = Database(db_id='theypsilon_unofficial_distribution', db_url='https://raw.githubusercontent.com/theypsilon/Distribution_Unofficial_MiSTer/main/unofficialdb.json.zip', title='theypsilon Unofficial Distribution')
DB_LLAPI_FOLDER = Database(db_id='llapi_folder', db_url='https://raw.githubusercontent.com/MiSTer-LLAPI/LLAPI_folder_MiSTer/main/llapidb.json.zip', title='LLAPI Folder')
DB_ARCADE_OFFSET_FOLDER = Database(db_id='arcade_offset_folder', db_url='https://raw.githubusercontent.com/atrac17/Arcade_Offset/db/arcadeoffsetdb.json.zip', title='Arcade Offset folder')
DB_COIN_OP_COLLECTION = Database(db_id='atrac17/Coin-Op_Collection', db_url='https://raw.githubusercontent.com/atrac17/Coin-Op_Collection/db/db.json.zip', title='Coin-Op Collection')

DB_ID_NAMES_TXT = 'names_txt'
DB_NAMES_CHAR54_MANUFACTURER_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR54_Manufacturer_EU.json', title='Names TXT: CHAR54 Manufacturer EU')
DB_NAMES_CHAR28_MANUFACTURER_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Manufacturer_EU.json', title='Names TXT: CHAR28 Manufacturer EU')
DB_NAMES_CHAR28_MANUFACTURER_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Manufacturer_US.json', title='Names TXT: CHAR28 Manufacturer US')
DB_NAMES_CHAR28_MANUFACTURER_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Manufacturer_JP.json', title='Names TXT: CHAR28 Manufacturer JP')
DB_NAMES_CHAR28_COMMON_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Common_EU.json', title='Names TXT: CHAR28 Common EU')
DB_NAMES_CHAR28_COMMON_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Common_US.json', title='Names TXT: CHAR28 Common US')
DB_NAMES_CHAR28_COMMON_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR28_Common_JP.json', title='Names TXT: CHAR28 Common JP')
DB_NAMES_CHAR18_MANUFACTURER_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Manufacturer_EU.json', title='Names TXT: CHAR18 Manufacturer EU')
DB_NAMES_CHAR18_MANUFACTURER_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Manufacturer_US.json', title='Names TXT: CHAR18 Manufacturer US')
DB_NAMES_CHAR18_MANUFACTURER_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Manufacturer_JP.json', title='Names TXT: CHAR18 Manufacturer JP')
DB_NAMES_CHAR18_COMMON_EU_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Common_EU.json', title='Names TXT: CHAR18 Common EU')
DB_NAMES_CHAR18_COMMON_US_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Common_US.json', title='Names TXT: CHAR18 Common US')
DB_NAMES_CHAR18_COMMON_JP_TXT = Database(db_id=DB_ID_NAMES_TXT, db_url='https://raw.githubusercontent.com/ThreepwoodLeBrush/Names_MiSTer/dbs/names_CHAR18_Common_JP.json', title='Names TXT: CHAR18 Common JP')


_names_dict = {
    'JP': {
        'CHAR18': {
            'Common': DB_NAMES_CHAR18_COMMON_JP_TXT,
            'Manufacturer': DB_NAMES_CHAR18_MANUFACTURER_JP_TXT
        },
        'CHAR28': {
            'Common': DB_NAMES_CHAR28_COMMON_JP_TXT,
            'Manufacturer': DB_NAMES_CHAR28_MANUFACTURER_JP_TXT
        }
    },
    'US': {
        'CHAR18': {
            'Common': DB_NAMES_CHAR18_COMMON_US_TXT,
            'Manufacturer': DB_NAMES_CHAR18_MANUFACTURER_US_TXT
        },
        'CHAR28': {
            'Common': DB_NAMES_CHAR28_COMMON_US_TXT,
            'Manufacturer': DB_NAMES_CHAR28_MANUFACTURER_US_TXT
        }
    },
    'EU': {
        'CHAR18': {
            'Common': DB_NAMES_CHAR18_COMMON_EU_TXT,
            'Manufacturer': DB_NAMES_CHAR18_MANUFACTURER_EU_TXT
        },
        'CHAR28': {
            'Common': DB_NAMES_CHAR28_COMMON_EU_TXT,
            'Manufacturer': DB_NAMES_CHAR28_MANUFACTURER_EU_TXT
        },
        'CHAR54': {
            'Manufacturer': DB_NAMES_CHAR54_MANUFACTURER_EU_TXT
        }
    }
}


def db_names_txt_by_locale(region: str, char_code: str, sort_code: str) -> Database:
    return _names_dict.get(region, {}).get(char_code, {}).get(sort_code, DB_NAMES_CHAR18_COMMON_JP_TXT)


def names_locale_by_db_url(db_url) -> (str, str, str):
    for region in _names_dict:
        for char_code in _names_dict[region]:
            for sort_code, db in _names_dict[region][char_code].items():
                if db_url == db.db_url:
                    return region, char_code, sort_code

    if db_url == DB_NAMES_CHAR18_COMMON_JP_TXT.db_url:
        raise ValueError('Could not find a value for DB_NAMES_CHAR18_COMMON_JP_TXT')

    return names_locale_by_db_url(DB_NAMES_CHAR18_COMMON_JP_TXT.db_url)


DB_TTY2OLED_FILES = Database(db_id='tty2oled_files', db_url='https://raw.githubusercontent.com/venice1200/MiSTer_tty2oled/main/tty2oleddb.json', title='tty2oled files')
DB_I2C2OLED_FILES = Database(db_id='i2c2oled_files', db_url='https://raw.githubusercontent.com/venice1200/MiSTer_i2c2oled/main/i2c2oleddb.json', title='i2c2oled files')
DB_MISTERSAM_FILES = Database(db_id='MiSTer_SAM_files', db_url='https://raw.githubusercontent.com/mrchrisster/MiSTer_SAM/main/MiSTer_SAMdb.json', title='MiSTer SAM files')
DB_BIOS = Database(db_id='bios_db', db_url='https://raw.githubusercontent.com/theypsilon/BiosDB_MiSTer/db/bios_db.json', title='BIOS Database')
DB_ARCADE_ROMS = Database(db_id='arcade_roms_db', db_url='https://raw.githubusercontent.com/theypsilon/ArcadeROMsDB_MiSTer/db/arcade_roms_db.json.zip', title='Arcade ROMs Database')
