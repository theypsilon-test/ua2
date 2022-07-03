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

from update_all.config import Config
from update_all.constants import DOWNLOADER_INI_STANDARD_PATH
from update_all.update_all_service import UpdateAllService
from test.fake_filesystem import FileSystemFactory
from test.file_system_tester_state import FileSystemState
from test.update_all_service_tester import UpdateAllServiceFactoryTester, UpdateAllServiceTester, ConfigReaderTester
import unittest


def tester(files=None, folders=None, config: Config = None):
    state = FileSystemState(files=files, folders=folders)
    config_reader_tester = ConfigReaderTester(config=config)
    return UpdateAllServiceTester(config_reader=config_reader_tester, file_system=FileSystemFactory(state=state).create_for_system_scope()), state


class TestUpdateAllService(unittest.TestCase):
    def test_factory_create___on_default_environment___returns_update_all_service(self):
        self.assertIsInstance(UpdateAllServiceFactoryTester().create({}), UpdateAllService)

    def test_full_run___on_empty_environment___returns_0(self):
        sut, _ = tester()
        self.assertEqual(0, sut.full_run())

    def test_full_run___on_empty_environment___writes_default_downloader_ini(self):
        sut, fs = tester()
        sut.full_run()
        self.assertEqual(Path('test/fixtures/default_downloader.ini').read_text(), fs.files[DOWNLOADER_INI_STANDARD_PATH]['content'])

    def test_full_run___over_dirty_downloader_ini_after_changing_some_options___writes_changed_downloader(self):
        sut, fs = tester(files={
            DOWNLOADER_INI_STANDARD_PATH: {'content': Path('test/fixtures/dirty_downloader.ini').read_text()}
        }, config=Config(main_updater=False, llapi_updater=True, names_region='EU', names_char_code='CHAR28', names_sort_code='Manufacturer', download_beta_cores=True))
        sut.full_run()
        self.assertEqual(Path('test/fixtures/changed_downloader.ini').read_text(), fs.files[DOWNLOADER_INI_STANDARD_PATH]['content'])
