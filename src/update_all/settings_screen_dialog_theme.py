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
import abc
import curses
from typing import Optional, Dict, Any

from update_all.ui_engine import UiTheme, UiSection, EffectChain, Interpolator, ProcessKeyResult
from update_all.ui_engine_client_helpers import NavigationState, make_action_effect_chain


class SettingsScreenDialogTheme(UiTheme):
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
        drawer = _UiNakedPostDrawer(window, interpolator)
        if ui_type == 'menu':
            return _Menu(drawer, data, state)
        elif ui_type == 'confirm':
            return _Confirm(drawer, data, state)
        elif ui_type == 'message':
            if 'effects' not in data:
                data['effects'] = [{"type": "navigate", "target": "back"}]
            return _Message(drawer, data)
        else:
            raise ValueError(f'Not implemented ui_type: {ui_type}')


class UiDrawer(abc.ABC):
    def start(self):
        """"Start of screen"""

    def write_line(self, text, is_selected=False):
        """"Write line (row)"""

    def next_line(self):
        """"Jumps one line (row)"""

    def end_columns_in_line(self):
        """"Finalizes column entries for current line"""

    def write_column(self, text, is_selected=False):
        """"Write column on current line"""

    def flush(self) -> int:
        """"Flushes all screen UI and returns char"""


class _UiNakedJitDrawer(UiDrawer):
    def __init__(self, window, interpolator: Interpolator):
        self._window = window
        self._interpolator = interpolator
        self._line_cursor = 0
        self._column_cursor = 0

    def start(self):
        self._line_cursor = 0
        self._column_cursor = 0

    def write_line(self, text, is_selected=False):
        self._window.addstr(self._line_cursor, 1, self._interpolator.interpolate(text), curses.A_REVERSE if is_selected else curses.A_NORMAL)
        self.next_line()

    def next_line(self):
        self._line_cursor += 1
        self._column_cursor = 0

    def end_columns_in_line(self):
        if self._column_cursor > 0:
            self._line_cursor += 1
            self._column_cursor = 0

    def write_column(self, text, is_selected=False):
        self._window.addstr(self._line_cursor, 1 + 30 * self._column_cursor, self._interpolator.interpolate(text), curses.A_REVERSE if is_selected else curses.A_NORMAL)
        self._column_cursor += 1

    def flush(self):
        return self._window.getch()


class _UiNakedPostDrawer(UiDrawer):
    def __init__(self, window, interpolator: Interpolator):
        self._window = window
        self._interpolator = interpolator
        self._lines = []
        self._rows = []

    def start(self):
        self._lines = []
        self._rows = []

    def write_line(self, text, is_selected=False):
        self.end_columns_in_line()
        interpolated_text = self._interpolator.interpolate(text)
        for line in interpolated_text.split('\n'):
            self._lines.append([(line, is_selected)])

    def next_line(self):
        self._lines.append([])

    def end_columns_in_line(self):
        if len(self._rows) > 0:
            self._lines.append(self._rows)
            self._rows = []

    def write_column(self, text, is_selected=False):
        self._rows.append((self._interpolator.interpolate(text), is_selected))

    def flush(self):
        self.end_columns_in_line()

        total_lines = len(self._lines)
        row_start = int(curses.COLS / 2 - calculate_wider_line(self._lines) / 2)

        line_index = int(curses.LINES / 2 - total_lines / 2)
        for line in self._lines:
            row_index = 0
            for row in line:
                text, is_selected = row
                width = calculate_column_width(self._lines, row_index - 1)

                self._window.addstr(line_index, row_start + width * row_index, text, curses.A_REVERSE if is_selected else curses.A_NORMAL)

                row_index += 1

            line_index += 1

        return self._window.getch()


def calculate_wider_line(lines):

    max_wide = 0

    for i in range(calculate_column_amounts(lines) + 1):
        max_wide += calculate_column_width(lines, i)

    return max_wide


def calculate_column_amounts(lines):
    amount = 0

    for line in lines:
        if len(line) > amount:
            amount = len(line)

    return amount


def calculate_column_width(lines, row_check):
    width = 0

    for line in lines:
        for row_index, row in enumerate(line):
            if row_index != row_check:
                continue

            text, _ = row
            if len(text) > width:
                width = len(text)

    return width + 2


class _Message(UiSection):
    def __init__(self, drawer: UiDrawer, data: Dict[str, Any]):
        self._drawer = drawer
        self._data = data

    def process_key(self) -> Optional[ProcessKeyResult]:
        self._drawer.start()

        if 'header' in self._data:
            self._drawer.write_line(self._data['header'])

        for index, text_line in enumerate(self._data['text']):
            self._drawer.write_line(text_line)

        self._drawer.write_line(self._data.get('action_name', 'Ok'), is_selected=True)

        key = self._drawer.flush()
        if key in [curses.KEY_ENTER, ord("\n")]:
            return EffectChain(self._data['effects'])

        return key

    def reset(self) -> None:
        pass


class _Confirm(UiSection):
    def __init__(self, drawer: UiDrawer, data: Dict[str, Any], state: NavigationState):
        self._drawer = drawer
        self._data = data
        self._state = state

    def process_key(self) -> Optional[ProcessKeyResult]:
        self._drawer.start()
        self._drawer.write_line(self._data['header'])

        for index, text_line in enumerate(self._data['text']):
            self._drawer.write_line(text_line)

        for index, action in enumerate(self._data['actions']):
            self._drawer.write_column(action['title'], index == self._state.lateral_position())

        key = self._drawer.flush()
        if key == curses.KEY_LEFT:
            self._state.navigate_left()
        elif key == curses.KEY_RIGHT:
            self._state.navigate_right()
        elif key in [curses.KEY_ENTER, ord("\n")]:
            return make_action_effect_chain(self._data, self._state)

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
    def __init__(self, drawer: UiDrawer, data: Dict[str, Any], state: NavigationState):
        self._drawer = drawer
        self._data = data
        self._state = state

    def process_key(self) -> Optional[ProcessKeyResult]:
        self._drawer.start()
        self._drawer.write_line(self._data['header'])

        for index, entry in enumerate(self._data['entries']):
            self._drawer.write_column(entry['title'], index == self._state.position())
            self._drawer.write_column(entry.get('description', ''), index == self._state.position())
            self._drawer.end_columns_in_line()

        for index, action in enumerate(self._data['actions']):
            self._drawer.write_column(action['title'], index == self._state.lateral_position())

        key = self._drawer.flush()
        if key == curses.KEY_UP:
            self._state.navigate_up()
        elif key == curses.KEY_DOWN:
            self._state.navigate_down()
        elif key == curses.KEY_LEFT:
            self._state.navigate_left()
        elif key == curses.KEY_RIGHT:
            self._state.navigate_right()
        elif key in [curses.KEY_ENTER, ord("\n")]:
            return make_action_effect_chain(self._data, self._state)

        return key

    def reset(self) -> None:
        self._state.reset_lateral_position()

