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

# Default SSL option
from enum import unique, Enum

DEFAULT_CACERT_FILE = '/etc/ssl/certs/cacert.pem'
DEFAULT_CURL_SSL_OPTIONS = '--cacert %s' % DEFAULT_CACERT_FILE
DEFAULT_COMMIT = 'unknown'

# Downloader files
FILE_update_all_storage = 'Scripts/.config/update_all/update_all.json.zip'
FILE_update_all_log = 'Scripts/.config/update_all/update_all.log'
FILE_update_all_ini = 'Scripts/update_all.ini'
FILE_MiSTer = 'MiSTer'
FILE_MiSTer_ini = 'MiSTer.ini'
FOLDER_scripts = 'Scripts'

# Reboot files
FILE_downloader_needs_reboot_after_linux_update = '/tmp/downloader_needs_reboot_after_linux_update'
FILE_mister_downloader_needs_reboot = '/tmp/MiSTer_downloader_needs_reboot'

MEDIA_FAT = '/media/fat'

# Dictionary Keys:

# Config
K_BASE_PATH = 'base_path'
K_BASE_SYSTEM_PATH = 'base_system_path'
K_STORAGE_PRIORITY = 'storage_priority'
K_DATABASES = 'databases'
K_ALLOW_DELETE = 'allow_delete'
K_ALLOW_REBOOT = 'allow_reboot'
K_UPDATE_LINUX = 'update_linux'
K_PARALLEL_UPDATE = 'parallel_update'
K_DOWNLOADER_SIZE_MB_LIMIT = 'downloader_size_mb_limit'
K_DOWNLOADER_PROCESS_LIMIT = 'downloader_process_limit'
K_DOWNLOADER_TIMEOUT = 'downloader_timeout'
K_DOWNLOADER_RETRIES = 'downloader_retries'
K_ZIP_FILE_COUNT_THRESHOLD = 'zip_file_count_threshold'
K_ZIP_ACCUMULATED_MB_THRESHOLD = 'zip_accumulated_mb_threshold'
K_FILTER = 'filter'
K_VERBOSE = 'verbose'
K_CONFIG_PATH = 'config_path'
K_USER_DEFINED_OPTIONS = 'user_defined_options'
K_CURL_SSL = 'curl_ssl'
K_DB_URL = 'db_url'
K_SECTION = 'section'
K_OPTIONS = 'options'
K_DEBUG = 'debug'
K_FAIL_ON_FILE_ERROR = 'fail_on_file_error'
K_COMMIT = 'commit'
K_UPDATE_LINUX_ENVIRONMENT = 'update_linux_environment'
K_DEFAULT_DB_ID = 'default_db_id'
K_START_TIME = 'start_time'

# Update All old options
## "Updaters"
K_MAIN_UPDATER = "main_updater"
K_JOTEGO_UPDATER = "jotego_updater"
K_UNOFFICIAL_UPDATER = "unofficial_updater"
K_LLAPI_UPDATER = "llapi_updater"
K_ARCADE_OFFSET_DOWNLOADER = "arcade_offset_downloader"
K_COIN_OP_COLLECTION_DOWNLOADER = "coin_op_collection_downloader"
K_ARCADE_ROMS_DB_DOWNLOADER = "arcade_roms_db_downloader"
K_TTY2OLED_FILES_DOWNLOADER = "tty2oled_files_downloader"
K_I2C2OLED_FILES_DOWNLOADER = "i2c2oled_files_downloader"
K_MISTERSAM_FILES_DOWNLOADER = "mistersam_files_downloader"
K_BIOS_GETTER = "bios_getter"
K_MAME_GETTER = "mame_getter"
K_HBMAME_GETTER = "hbmame_getter"
K_NAMES_TXT_UPDATER = "names_txt_updater"
K_ARCADE_ORGANIZER = "arcade_organizer"

## Options
K_ENCC_FORKS = "encc_forks"
K_DOWNLOAD_BETA_CORES = "download_beta_cores"

## Misc
K_COUNTDOWN_TIME = "countdown_time"
K_WAIT_TIME_FOR_READING = "wait_time_for_reading"
K_AUTOREBOOT = "autoreboot"
K_KEEP_USBMOUNT_CONF = "keep_usbmount_conf"
K_NAMES_REGION = "names_region"
K_NAMES_CHAR_CODE = "names_char_code"
K_NAMES_SORT_CODE = "names_sort_code"


# Env
KENV_CURRENT_PATH = 'CURRENT_PATH'
KENV_CURL_SSL = 'CURL_SSL'
KENV_COMMIT = 'COMMIT'
KENV_NOT_MISTER = 'NOT_MISTER'

@unique
class PathType(Enum):
    FILE = 0
    FOLDER = 1


# Update All old constants
UPDATE_ALL_VERSION = "2.0"
UPDATE_ALL_PC_UPDATER = "false"
UPDATE_ALL_OS = "MiSTer_Linux"
UPDATE_ALL_LAUNCHER_MD5 = "ac10fbada40e3e5f133bc0eee0dd53d5"
UPDATE_ALL_PATREON_KEY_PATH = "Scripts/update_all.patreonkey"
UPDATE_ALL_PATREON_KEY_SIZE = 16384
UPDATE_ALL_PATREON_KEY_MD5Q0 = "00e9f6acaec74650ddd38a14334ebaef"
SETTINGS_ON_FILENAME = "settings-on"
WORK_PATH = "Scripts/.config/update_all"
MISTER_DOWNLOADER_WORK_FOLDER = "Scripts/.config/downloader"
ARCADE_ORGANIZER_INSTALLED_NAMES_TXT = "Scripts/.config/arcade-organizer/installed_names.txt"
ARCADE_ORGANIZER_FOLDER_OPTION_1 = "_Arcade/_Organized"
ARCADE_ORGANIZER_FOLDER_OPTION_2 = "_Arcade"
ARCADE_ORGANIZER_FOLDER_OPTION_3 = "_Arcade Organized"
MISTER_INI_PATH = "MiSTer.ini"
NAMES_TXT_PATH = "names.txt"
UPDATE_ALL_URL = "https://raw.githubusercontent.com/theypsilon/Update_All_MiSTer/master/update_all.sh"
ARCADE_ORGANIZER_INI = "Scripts/update_arcade-organizer.ini"
DOWNLOADER_URL = "https://github.com/MiSTer-devel/Downloader_MiSTer/releases/download/latest/dont_download.zip"
ARCADE_ORGANIZER_URL = "https://raw.githubusercontent.com/theypsilon/_arcade-organizer/master/_arcade-organizer.sh"
DOWNLOADER_INI_STANDARD_PATH = "downloader.ini"
TEST_UNSTABLE_SPINNER_FIRMWARE_MD5 = "cc0518143d90f5662d27f140f3f3d697"
FILE_MiSTer_version = '/MiSTer.version'
