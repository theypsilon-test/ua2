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
from typing import Dict, Any

from update_all.ui_engine import EffectChain


class NavigationState:
    def __init__(self, vertical_limit, horizontal_limit):
        self._position = 0
        self._lateral_position = 0
        self._vertical_limit = vertical_limit
        self._horizontal_limit = horizontal_limit

    def position(self):
        return self._position

    def lateral_position(self):
        return self._lateral_position

    def navigate_up(self):
        self._position -= 1
        if self._position < 0:
            self._position = 0

    def navigate_down(self):
        self._position += 1
        if self._position >= self._vertical_limit:
            self._position = self._vertical_limit - 1

    def navigate_left(self):
        self._lateral_position -= 1
        if self._lateral_position < 0:
            self._lateral_position = 0

    def navigate_right(self):
        self._lateral_position += 1
        if self._lateral_position >= self._horizontal_limit:
            self._lateral_position = self._horizontal_limit - 1

    def reset_lateral_position(self, value=None):
        self._lateral_position = value or 0

    def reset_position(self, value=None):
        self._position = value or 0


def make_action_effect_chain(data: Dict[str, Any], state: NavigationState) -> EffectChain:
    props = data['actions'][state.lateral_position()]
    if props['type'] == 'symbol':
        selection = data['entries'][state.position()]
        if 'actions' not in selection:
            raise ValueError('Selection does not contain nested actions that can be linked to symbol.')
        return EffectChain(selection['actions'][props['symbol']])
    elif props['type'] == 'fixed':
        return EffectChain(props['fixed'])
    else:
        raise Exception(f"Action type '{props['type']}' not valid.")
