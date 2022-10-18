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
import unittest
from pathlib import Path

from test.fake_filesystem import FileSystemFactory
from test.file_system_tester_state import FileSystemState
from test.update_all_service_tester import TransitionServiceTester, local_store
from update_all.config import Config
from update_all.constants import MEDIA_FAT, DOWNLOADER_INI_STANDARD_PATH, FILE_update_all_ini, \
    FILE_update_names_txt_ini, FILE_update_jtcores_ini, ARCADE_ORGANIZER_INI

downloader_ini = f'{MEDIA_FAT}/{DOWNLOADER_INI_STANDARD_PATH}'
update_all_ini = f'{MEDIA_FAT}/{FILE_update_all_ini}'
update_names_txt_ini = f'{MEDIA_FAT}/{FILE_update_names_txt_ini}'
update_jtcores_ini = f'{MEDIA_FAT}/{FILE_update_jtcores_ini}'
update_arcade_organizer_ini = f'{MEDIA_FAT}/{ARCADE_ORGANIZER_INI}'


def test_transition_from_update_all_1(files=None):
    config = Config()
    fs = FileSystemState(config=config, files=files)
    sut = TransitionServiceTester(file_system=FileSystemFactory(state=fs).create_for_system_scope())
    sut.transition_from_update_all_1(config, local_store())
    return fs

class TestTransitionService(unittest.TestCase):
    def test_on_empty_state___writes_default_downloader_ini(self):
        fs = test_transition_from_update_all_1()
        self.assertEqual(Path('test/fixtures/downloader_ini/default_downloader.ini').read_text(), fs.files[downloader_ini]['content'])

    def test_with_dirty_downloader_ini___writes_nothing(self):
        fs = test_transition_from_update_all_1(files={downloader_ini: {'content': Path(
            'test/fixtures/downloader_ini/dirty_downloader.ini').read_text()}})
        self.assertEqual(Path('test/fixtures/downloader_ini/dirty_downloader.ini').read_text(), fs.files[downloader_ini]['content'])

    def test_with_downloader_ini_and_other_inis___keeps_downloader_ini(self):
        fs = test_transition_from_update_all_1(files={
            downloader_ini: {'content': Path('test/fixtures/downloader_ini/default_downloader.ini').read_text()},
            update_all_ini: {'content': Path('test/fixtures/update_all_ini/complete_ua.ini').read_text()},
        })
        self.assertEqual({
            downloader_ini: {'content': Path('test/fixtures/downloader_ini/default_downloader.ini').read_text()}
        }, fs.files)

    def test_with_update_all_ini___keeps_downloader_ini(self):
        fs = test_transition_from_update_all_1(files={
            update_all_ini: {'content': Path('test/fixtures/update_all_ini/complete_ua.ini').read_text()},
            update_names_txt_ini: {'content': Path('test/fixtures/update_names-txt_ini/complete_nt.ini').read_text()},
            update_jtcores_ini: {'content': Path('test/fixtures/update_jtcores_ini/complete_jt.ini').read_text()},
        })
        self.assertEqual({
            downloader_ini: {
                'content': Path('test/fixtures/downloader_ini/complete_downloader.ini').read_text(),
                'hash': 'downloader.ini',
                'size': 1
            },
            update_arcade_organizer_ini.lower(): {
                'content': Path('test/fixtures/update_arcade-organizer_ini/complete_ao.ini').read_text(),
                'hash': 'Scripts/update_arcade-organizer.ini',
                'size': 1
            }
        }, fs.files)
