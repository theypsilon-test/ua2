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
DEFAULT_INI_PATH = '/media/fat/Scripts/update_all.ini'
DEFAULT_COMMIT = 'unknown'

# Downloader files
FILE_update_all_storage = 'Scripts/.config/update_all/update_all.json.zip'
FILE_update_all_log = 'Scripts/.config/update_all/update_all.log'

# Reboot files
FILE_downloader_needs_reboot_after_linux_update = '/tmp/downloader_needs_reboot_after_linux_update'
FILE_mister_downloader_needs_reboot = '/tmp/MiSTer_downloader_needs_reboot'


# Standard Drives
MEDIA_USB0 = '/media/usb0'
MEDIA_USB1 = '/media/usb1'
MEDIA_USB2 = '/media/usb2'
MEDIA_USB3 = '/media/usb3'
MEDIA_USB4 = '/media/usb4'
MEDIA_USB5 = '/media/usb5'
MEDIA_FAT_CIFS = '/media/fat/cifs'
MEDIA_FAT = '/media/fat'

# Storage Priority Resolution Sequence
STORAGE_PATHS_PRIORITY_SEQUENCE = [
    MEDIA_USB0,
    MEDIA_USB1,
    MEDIA_USB2,
    MEDIA_USB3,
    MEDIA_USB4,
    MEDIA_USB5,
    MEDIA_FAT_CIFS,
    MEDIA_FAT
]


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

# Env
KENV_INI_PATH = 'INI_PATH'
KENV_CURL_SSL = 'CURL_SSL'
KENV_COMMIT = 'COMMIT'


@unique
class PathType(Enum):
    FILE = 0
    FOLDER = 1
