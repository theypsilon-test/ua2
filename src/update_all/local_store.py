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
from typing import Optional, Dict, Union


class LocalStore:
    def __init__(self, props: Dict[str, Union[str, bool]]):
        self._props = props
        self._dirty = False

    def set_theme(self, theme: str) -> None:
        self._props['theme'] = theme
        self._mark_force_save()

    def get_theme(self) -> Optional[str]:
        return self._props['theme']

    def set_download_beta_cores(self, download_beta_cores: bool) -> None:
        self._props['download_beta_cores'] = download_beta_cores
        self._mark_force_save()

    def get_download_beta_cores(self) -> Optional[bool]:
        return self._props['download_beta_cores']

    def set_names_region(self, names_region: str) -> None:
        self._props['names_region'] = names_region
        self._mark_force_save()

    def get_names_region(self) -> Optional[str]:
        return self._props['names_region']

    def set_names_char_code(self, names_char_code: str) -> None:
        self._props['names_char_code'] = names_char_code
        self._mark_force_save()

    def get_names_char_code(self) -> Optional[str]:
        return self._props['names_char_code']

    def set_names_sort_code(self, names_sort_code: str) -> None:
        self._props['names_sort_code'] = names_sort_code
        self._mark_force_save()

    def get_names_sort_code(self) -> Optional[str]:
        return self._props['names_sort_code']

    def unwrap_props(self):
        return self._props

    def needs_save(self):
        return self._dirty

    def _mark_force_save(self):
        self._dirty = True
