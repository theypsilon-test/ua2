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
from pathlib import Path

from update_all.constants import MEDIA_FAT, DOWNLOADER_INI_STANDARD_PATH, FILE_update_all_ini, \
    FILE_update_names_txt_ini, FILE_update_jtcores_ini, ARCADE_ORGANIZER_INI


downloader_ini = f'{MEDIA_FAT}/{DOWNLOADER_INI_STANDARD_PATH}'
update_all_ini = f'{MEDIA_FAT}/{FILE_update_all_ini}'
update_names_txt_ini = f'{MEDIA_FAT}/{FILE_update_names_txt_ini}'
update_jtcores_ini = f'{MEDIA_FAT}/{FILE_update_jtcores_ini}'
update_arcade_organizer_ini = f'{MEDIA_FAT}/{ARCADE_ORGANIZER_INI}'

def default_downloader_ini_content():
    return Path('test/fixtures/downloader_ini/default_downloader.ini').read_text()
