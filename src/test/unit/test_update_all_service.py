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
from update_all.constants import DOWNLOADER_INI_STANDARD_PATH, MEDIA_FAT
from update_all.update_all_service import UpdateAllService
from test.fake_filesystem import FileSystemFactory
from test.file_system_tester_state import FileSystemState
from test.update_all_service_tester import UpdateAllServiceFactoryTester, UpdateAllServiceTester, ConfigReaderTester, \
    default_env
import unittest


def tester(files=None, folders=None, config: Config = None):
    state = FileSystemState(files=files, folders=folders)
    config_reader_tester = ConfigReaderTester(config=config or Config())
    return UpdateAllServiceTester(config_reader=config_reader_tester, file_system=FileSystemFactory(state=state).create_for_system_scope()), state


downloader_ini = f'{MEDIA_FAT}/{DOWNLOADER_INI_STANDARD_PATH}'


class TestUpdateAllService(unittest.TestCase):
    def test_factory_create___on_default_environment___returns_update_all_service(self):
        self.assertIsInstance(UpdateAllServiceFactoryTester().create(default_env()), UpdateAllService)

    def test_full_run___on_empty_environment___returns_0(self):
        sut, _ = tester()
        self.assertEqual(0, sut.full_run())

    def test_full_run___on_empty_environment___writes_default_downloader_ini(self):
        sut, fs = tester()
        sut.full_run()
        self.assertEqual(Path('test/fixtures/default_downloader.ini').read_text(), fs.files[downloader_ini]['content'])

    def test_write_downloader_ini___over_dirty_downloader_ini_after_changing_some_options___writes_changed_downloader(self):
        config = Config(main_updater=False, llapi_updater=True, names_region='EU', names_char_code='CHAR28', names_sort_code='Manufacturer', download_beta_cores=True)
        sut, fs = tester(files={
            downloader_ini: {'content': Path('test/fixtures/dirty_downloader.ini').read_text()}
        }, config=config)
        sut.write_downloader_ini(config)
        sut.full_run()
        self.assertEqual(Path('test/fixtures/changed_downloader.ini').read_text(), fs.files[downloader_ini]['content'])

    def test_write_downloader_ini___over_bug_duplications_downloader_ini_after_changing_some_options___writes_changed_downloader(self):
        config = Config(download_beta_cores=True, names_region='EU', unofficial_updater=True, llapi_updater=True, arcade_roms_db_downloader=True, arcade_offset_downloader=True, tty2oled_files_downloader=True, i2c2oled_files_downloader=True, mistersam_files_downloader=True)
        sut, fs = tester(files={
            downloader_ini: {'content': Path('test/fixtures/bug_duplications_downloader.ini').read_text()}
        }, config=config)
        sut.write_downloader_ini(config)
        sut.full_run()
        self.assertEqual(Path('test/fixtures/bug_duplications_downloader.ini').read_text(), fs.files[downloader_ini]['content'])

    def test_write_downloader_ini___over_bug_names_txt_updater_disabled_downloader_ini_after_changing_some_options___writes_changed_downloader(self):
        config = Config(download_beta_cores=True, names_txt_updater=False, bios_getter=True, unofficial_updater=True, llapi_updater=True, arcade_roms_db_downloader=True, arcade_offset_downloader=True, tty2oled_files_downloader=True, i2c2oled_files_downloader=True, mistersam_files_downloader=True)
        sut, fs = tester(files={
            downloader_ini: {'content': Path('test/fixtures/bug_names_txt_updater_disabled_downloader.ini').read_text()}
        }, config=config)
        sut.write_downloader_ini(config)
        sut.full_run()
        self.assertEqual(Path('test/fixtures/bug_names_txt_updater_disabled_downloader.ini').read_text(), fs.files[downloader_ini]['content'])

    def test_write_downloader_ini___lower_case_coin_ops___becomes_uppercase_after_writing_downloader(self):
        sut, fs = tester(files={
            downloader_ini: {'content': Path('test/fixtures/coin_op_lowercase_downloader.ini').read_text()}
        }, config=Config())
        sut.write_downloader_ini(Config())
        sut.full_run()
        self.assertEqual(Path('test/fixtures/coin_op_uppercase_downloader.ini').read_text(), fs.files[downloader_ini]['content'])
