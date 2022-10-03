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

from update_all.ui_model_utilities import gather_default_values, list_variables_with_group


class TestUiModelsUtilities(unittest.TestCase):
    def test_gather_default_values(self):
        expected = {
            "update_all_version": 2,
            "names_region": "US",
            "arcade_offset_downloader": False
        }
        self.assertEqual(expected, gather_default_values(test_model()))

    def test_list_variables_with_group_x(self):
        expected = {"update_all_version": "version", "arcade_offset_downloader": "aod"}
        self.assertEqual(expected, list_variables_with_group(test_model(), 'x'))


def test_model(): return {
    "variables": {
        "update_all_version": {"default": "2", "rename": "version", "group": "x"},
    },
    "items": {
        "names_txt_menu": {
            "type": "dialog_sub_menu",
            "header": "Names TXT Settings",
            "variables": {
                "names_region": {"default": "US", "values": ["US", "EU", "JP"]},
            },
            "entries": []
        },
        "misc_menu": {
            "type": "dialog_sub_menu",
            "header": "Misc | Other Settings",
            "variables": {
                "arcade_offset_downloader": {"default": "false", "rename": "aod", "group": "x", "values": ["false", "true"]},
            },
            "entries": []
        }
    }
}
