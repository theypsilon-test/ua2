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
from typing import Tuple

from test.file_system_tester_state import FileSystemState
from test.unit.test_update_all_service import downloader_ini
from test.update_all_service_tester import SettingsScreenTester, UiStub
from update_all.config import Config, ConfigProvider
from test.fake_filesystem import FileSystemFactory
from update_all.settings_screen import SettingsScreen
from update_all.ui_engine import Ui


class TestSettingsScreen(unittest.TestCase):

    def test_calculate_needs_save___on_no_files_setup___returns_downloader_ini_changes(self) -> None:
        sut, ui, _ = tester()
        sut.calculate_needs_save(ui)
        self.assertEqual('  - downloader.ini', ui.get_value('needs_save_file_list'))
        self.assertEqual('true', ui.get_value('needs_save'))

    def test_save___on_no_files_setup___creates_default_downloader_ini(self) -> None:
        sut, ui, fs = tester()
        sut.save(ui)
        self.assertEqual(default_downloader_ini_content(), fs.files[downloader_ini]['content'])

    def test_calculate_needs_save___with_default_downloader_ini_and_disabled_names_txt_updater___returns_update_all_ini_and_downloader_ini_changes(self) -> None:
        sut, ui, _ = tester(files={downloader_ini: {'content': default_downloader_ini_content()}})
        ui.set_value('names_txt_updater', 'false')
        sut.calculate_needs_save(ui)
        self.assertEqual('  - downloader.ini\n  - update_all.ini', ui.get_value('needs_save_file_list'))
        self.assertEqual('true', ui.get_value('needs_save'))

    def test_calculate_needs_save___with_default_downloader_ini___returns_no_changes(self) -> None:
        sut, ui, _ = tester(files={downloader_ini: {'content': default_downloader_ini_content()}})
        sut.calculate_needs_save(ui)
        self.assertEqual('', ui.get_value('needs_save_file_list'))
        self.assertEqual('false', ui.get_value('needs_save'))

    def test_calculate_needs_save___with_bug_names_txt_updater_disabled_downloader_and_matching_options___returns_no_changes(self):
        config = Config(download_beta_cores=True, names_txt_updater=False, bios_getter=True, unofficial_updater=True, llapi_updater=True, arcade_roms_db_downloader=True, arcade_offset_downloader=True, tty2oled_files_downloader=True, i2c2oled_files_downloader=True, mistersam_files_downloader=True)
        sut, ui, _ = tester(files={
            downloader_ini: {'content': Path('test/fixtures/bug_names_txt_updater_disabled_downloader.ini').read_text()}
        }, config=config)
        sut.calculate_needs_save(ui)
        self.assertEqual('', ui.get_value('needs_save_file_list'))
        self.assertEqual('false', ui.get_value('needs_save'))


def tester(files=None, config=None) -> Tuple[SettingsScreen, Ui, FileSystemState]:
    ui = UiStub()
    state = FileSystemState(files=files)
    config_provider = ConfigProvider()
    config_provider.initialize(config or Config())
    settings_screen = SettingsScreenTester(config_provider=config_provider, file_system=FileSystemFactory(state=state).create_for_system_scope())
    settings_screen.initialize_ui(ui)

    return settings_screen, ui, state


def default_downloader_ini_content():
    return Path('test/fixtures/default_downloader.ini').read_text()
