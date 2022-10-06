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
import curses
from typing import Union, Optional, Dict, Any

from update_all.ui_engine import UiTheme, UiSection, EffectChain, Action, Interpolator
from update_all.ui_engine_client_helpers import NavigationState, make_action


class SettingsScreenNakedTheme(UiTheme):
    def initialize_theme(self, window: curses.window):
        window.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
        window.keypad(True)
        window.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def create_ui_section(self, ui_type: str, window: curses.window, data: Dict[str, Any], interpolator: Interpolator) -> UiSection:
        state = NavigationState(len(data.get('entries', {})), len(data.get('actions', {})))
        if ui_type == 'menu':
            return _Menu(window, data, state, interpolator)
        elif ui_type == 'confirm':
            return _Confirm(window, data, state, interpolator)
        elif ui_type == 'message':
            if 'effects' not in data:
                data['effects'] = [{"type": "navigate", "target": "back"}]
            return _Message(window, data, interpolator)
        else:
            raise ValueError(f'Not implemented ui_type: {ui_type}')


class _Message(UiSection):
    def __init__(self, window: curses.window, data: Dict[str, Any], interpolator: Interpolator):
        self._window = window
        self._data = data
        self._interpolator = interpolator

    def process_key(self) -> Optional[Union[int, EffectChain, Action]]:
        header_offset = 0
        if 'header' in self._data:
            self._window.addstr(0, 1, self._interpolator.interpolate(self._data['header']), curses.A_NORMAL)
            header_offset = 1

        for index, text_line in enumerate(self._data['text']):
            self._window.addstr(header_offset + index, 1, self._interpolator.interpolate(text_line), curses.A_NORMAL)

        self._window.addstr(header_offset + len(self._data['text']), 1, self._interpolator.interpolate(self._data.get('action_name', 'Ok')), curses.A_REVERSE)

        key = self._window.getch()
        if key in [curses.KEY_ENTER, ord("\n")]:
            return EffectChain(self._data['effects'])

        return key

    def reset(self) -> None:
        pass


class _Confirm(UiSection):
    def __init__(self, window: curses.window, data: Dict[str, Any], state: NavigationState, interpolator: Interpolator):
        self._window = window
        self._data = data
        self._state = state
        self._interpolator = interpolator

    def process_key(self) -> Optional[Union[int, EffectChain, Action]]:
        self._window.addstr(0, 1,  self._interpolator.interpolate(self._data['header']), curses.A_NORMAL)

        for index, text_line in enumerate(self._data['text']):
            self._window.addstr(1 + index, 1, self._interpolator.interpolate(text_line), curses.A_NORMAL)

        for index, action in enumerate(self._data['actions']):
            mode = curses.A_REVERSE if index == self._state.lateral_position() else curses.A_NORMAL
            self._window.addstr(1 + len(self._data['text']), 1 + 14 * index, self._interpolator.interpolate(action['title']), mode)

        key = self._window.getch()
        if key == curses.KEY_LEFT:
            self._state.navigate_left()
        elif key == curses.KEY_RIGHT:
            self._state.navigate_right()
        elif key in [curses.KEY_ENTER, ord("\n")]:
            return make_action(self._data, self._state)

        return key

    def reset(self) -> None:
        self._state.reset_lateral_position()
        if 'preselected_action' not in self._data:
            return

        preselected_action = self._data['preselected_action']
        for index, action in enumerate(self._data['actions']):
            if action['title'] == preselected_action:
                self._state.reset_lateral_position(index)


class _Menu(UiSection):
    def __init__(self, window: curses.window, data: Dict[str, Any], state: NavigationState, interpolator: Interpolator):
        self._window = window
        self._data = data
        self._state = state
        self._interpolator = interpolator

    def process_key(self) -> Optional[Union[int, EffectChain, Action]]:
        self._window.addstr(0, 1,  self._interpolator.interpolate(self._data['header']), curses.A_NORMAL)

        for index, entry in enumerate(self._data['entries']):
            mode = curses.A_REVERSE if index == self._state.position() else curses.A_NORMAL
            self._window.addstr(1 + index, 1,  self._interpolator.interpolate(entry['title']), mode)
            self._window.addstr(1 + index, 30,  self._interpolator.interpolate(entry.get('description', '')), mode)

        for index, action in enumerate(self._data['actions']):
            mode = curses.A_REVERSE if index == self._state.lateral_position() else curses.A_NORMAL
            self._window.addstr(1 + len(self._data['entries']), 1 + 14 * index,  self._interpolator.interpolate(action['title']), mode)

        key = self._window.getch()
        if key == curses.KEY_UP:
            self._state.navigate_up()
        elif key == curses.KEY_DOWN:
            self._state.navigate_down()
        elif key == curses.KEY_LEFT:
            self._state.navigate_left()
        elif key == curses.KEY_RIGHT:
            self._state.navigate_right()
        elif key in [curses.KEY_ENTER, ord("\n")]:
            return make_action(self._data, self._state)

        return key

    def reset(self) -> None:
        self._state.reset_lateral_position()

