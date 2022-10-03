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
from typing import Dict, Callable, List, Any


class Ui(abc.ABC):
    def get_value(self, key: str) -> str:
        """Gets value for variable on the given key"""

    def set_value(self, key: str, value: Any) -> None:
        """Sets value as string for variable on the given key"""

    def refresh_screen(self) -> None:
        """Refreshes UI Screen"""


class UiComponent(abc.ABC):
    def initialize_ui(self, ui: Ui):
        """Initializes the UI object"""

    def initialize_effects(self, ui: Ui, effects: Dict[str, Callable[[], None]]):
        """Initializes the effects dictionary if necessary"""


class _UiSystem(Ui):
    def __init__(self, window, entrypoint, model, ui_components):
        self._window = window
        self._section = entrypoint
        self._model = model
        self._ui_components = ui_components
        self._items = self._model['items']
        self._values = {k: v['default'] for k, v in self._model.get('variables', {}).items()}
        for item in self._model['items'].values():
            self._values.update({k: v['default'] for k, v in item.get('variables', {}).items()})
        self._section_states = {}
        self._history = []

    def get_value(self, key: str) -> str:
        return self._values[key]

    def set_value(self, key: str, value: Any) -> None:
        self._values[key] = str(value).lower()

    def refresh_screen(self) -> None:
        self._window.clear()

    def display(self):
        self._window.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
        self._window.keypad(1)
        self._window.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        for component in self._ui_components:
            component.initialize_ui(self)

        self._current_section_state().reset()

        while True:
            new_section = self._current_section_state().tick()

            self._window.refresh()
            curses.doupdate()

            if new_section is None:
                continue

            self._window.clear()

            if new_section == 'exit_and_run':
                break
            elif new_section == 'abort':
                exit(0)
            elif new_section == 'back':
                if len(self._history) == 0:
                    break
                self._section = self._history.pop()

            elif new_section == 'clear_window':
                continue
            elif isinstance(new_section, dict):
                self._push_history()
                self._section = '@temporary'
                self._section_states['@temporary'] = self._make_section_state(self._window, new_section, self._values, self._model, self._ui_components)
                self._section_states['@temporary'].reset()
            else:
                self._push_history()
                self._section = new_section
                self._current_section_state().reset()

    def _push_history(self):
        if self._section == '@temporary':
            return
        self._history.append(self._section)

    def _current_section_state(self):
        if self._section not in self._section_states:
            self._section_states[self._section] = self._make_section_state(self._window, self._items[self._section], self._values, self._model, self._ui_components)
        return self._section_states[self._section]

    def _make_section_state(self, window, data, values, model, ui_components):
        expand_type(data, model)

        data['formatters'] = {**data.get('formatters', {}), **model.get('formatters', {})}
        data['variables'] = {**data.get('variables', {}), **model.get('variables', {})}

        state = _State(len(data.get('entries', {})), len(data.get('actions', {})))
        interpolator = _Interpolator(data, values)
        effect_resolver = _EffectResolver(self, state, data, values)
        for component in ui_components:
            effect_resolver.add_ui_component(component)

        hotkeys = {}
        for hk in data.get('hotkeys', []):
            for key in hk['keys']:
                hotkeys[key] = hk['action']

        if data['type'] == 'menu':
            return _Menu(window, data, values, state, interpolator, effect_resolver, hotkeys)
        elif data['type'] == 'confirm':
            return _Confirm(window, data, values, state, interpolator, effect_resolver, hotkeys)
        elif data['type'] == 'message':
            if 'effects' not in data:
                data['effects'] = [{"type": "navigate", "target": "back"}]
            return _Message(window, data, values, state, interpolator, effect_resolver, hotkeys)
        else:
            raise ValueError(f'Not implemented item type "{data["type"]}"')


def expand_type(data, model):
    while data['type'] in model['base_types']:
        base_type = model['base_types'][data['type']]
        if 'type' not in base_type:
            raise ValueError('There must always be a type property within the base_types.')

        for key, content in base_type.items():
            if type(content) in (str, int, float, bool):
                data[key] = base_type[key]
            elif isinstance(content, list):
                data[key] = [*data.get(key, []), *base_type.get(key, [])]
            elif isinstance(content, dict):
                data[key] = {**data.get(key, []), **base_type.get(key, [])}
            else:
                raise ValueError(f'Can not inherit field {key} with content of type: {str(type(content))}')


class _State:
    def __init__(self, vertical_limit, horizontal_limit):
        self.position = 0
        self.lateral_position = 0
        self._vertical_limit = vertical_limit
        self._horizontal_limit = horizontal_limit

    def navigate_up(self):
        self.position -= 1
        if self.position < 0:
            self.position = 0

    def navigate_down(self):
        self.position += 1
        if self.position >= self._vertical_limit:
            self.position = self._vertical_limit - 1

    def navigate_left(self):
        self.lateral_position -= 1
        if self.lateral_position < 0:
            self.lateral_position = 0

    def navigate_right(self):
        self.lateral_position += 1
        if self.lateral_position >= self._horizontal_limit:
            self.lateral_position = self._horizontal_limit - 1

    def reset_lateral_position(self):
        self.lateral_position = 0

    def reset_position(self):
        self.position = 0


class _Interpolator:
    def __init__(self, data, values):
        self._data = data
        self._values = values

    def interpolate(self, text):
        reading_state = 0
        reading_value = ''
        reading_modifier = ''
        reading_arguments = []
        reading_current_argument = ''
        values = dict()

        for character in text:
            if reading_state == 0:
                if character == '{':
                    reading_state = 1
                    reading_value = ''

            elif reading_state == 1:
                if character == '}':
                    reading_state = 0
                    if reading_value in self._data['formatters']:
                        variable_type = self._data['formatters'][reading_value]
                        values[reading_value] = variable_type[self._values[reading_value]]
                    else:
                        values[reading_value] = self._values[reading_value]
                elif character == ':':
                    reading_state = 2
                    reading_modifier = ''
                else:
                    reading_value += character

            elif reading_state == 2:
                if character == '=':
                    if reading_modifier not in self._data['formatters']:
                        raise NotImplementedError(f'Modifier "{reading_modifier}" is not in formatters.')

                    reading_arguments = []
                    reading_current_argument = ''
                    reading_state = 3
                elif character == '}':
                    reading_state = 0
                    if reading_modifier == 'bool':
                        values[reading_value + ':bool'] = 'true' if bool(self._values[reading_value]) else 'false'
                    elif reading_modifier in self._data['formatters']:
                        variable_type = self._data['formatters'][reading_modifier]
                        try:
                            values[reading_value + ':' + reading_modifier] = variable_type[self._values[reading_value]]
                        except Exception as e:
                            raise ValueError(reading_value, reading_modifier, variable_type, e)
                    else:
                        raise NotImplementedError(f'Modifier "{reading_modifier}" does not exit.')
                else:
                    reading_modifier += character

            elif reading_state == 3:
                if character == '}':
                    reading_arguments.append(reading_current_argument)
                    reading_state = 0
                    variable_type = self._data['formatters'][reading_modifier]
                    try:
                        values[reading_value + ':' + reading_modifier + '=' + ','.join(reading_arguments)] = variable_type[self._values[reading_value]].format(*reading_arguments)
                    except Exception as e:
                        raise ValueError(reading_value, reading_modifier, variable_type, reading_arguments, e)
                elif character == ',':
                    reading_arguments.append(reading_current_argument)
                    reading_current_argument = ''
                else:
                    reading_current_argument += character

            else:
                raise NotImplementedError(reading_state)

        for var_name, var_value in values.items():
            text = text.replace("{" + var_name + "}", str(var_value))
        return text


class _EffectResolver:
    def __init__(self, ui, state, data, values):
        self._ui = ui
        self._state = state
        self._data = data
        self._values = values
        self._additional_effects = {}

    def add_ui_component(self, ui_component):
        ui_component.initialize_effects(self._ui, self._additional_effects)

    def resolve_effect_chain(self, chain):
        result = None
        for effect in chain:
            if effect['type'] == 'condition':
                variable = effect['variable']
                return self.resolve_effect_chain(effect[self._values[variable]])
            elif effect['type'] == 'navigate':
                return effect['target']
            elif effect['type'] == 'select':
                for index, entry in enumerate(self._data['entries']):
                    if 'id' not in entry or entry['id'] != effect['target']:
                        continue

                    self._state.position = index
                    break
            elif effect['type'] == 'rotate_variable':
                target_variable = effect['target']
                possible_values = self._data['variables'][target_variable]['values']

                cur_index = 0
                for index, var_value in enumerate(possible_values):
                    if var_value == self._values[target_variable]:
                        cur_index = index
                        break

                cur_index += 1
                if cur_index >= len(possible_values):
                    cur_index = 0

                if possible_values[cur_index] != self._values[target_variable]:
                    self._values[target_variable] = possible_values[cur_index]
                    result = 'clear_window'
            elif effect['type'] in ('menu', 'message', 'confirm'):
                return effect
            elif effect['type'] in self._additional_effects:
                self._additional_effects[effect['type']](effect)
            else:
                raise NotImplementedError(f'Wrong effect type :"{effect["type"]}"')

        return result

    def resolve_action(self, action):
        if action['type'] == 'symbol':
            current_selection = self._data['entries'][self._state.position]
            return self.resolve_effect_chain(current_selection['actions'][action['symbol']])
        elif action['type'] == 'fixed':
            return self.resolve_effect_chain(action['fixed'])
        else:
            raise NotImplementedError(f'Wrong action type :"{action["type"]}"')


class _Message:
    def __init__(self, window, data, values, state, interpolator, effect_resolver, hotkeys):
        self._window = window
        self._data = data
        self._state = state
        self._hotkeys = hotkeys
        self._values = values
        self._interpolator = interpolator
        self._effect_resolver = effect_resolver

    def tick(self):
        header_offset = 0
        if 'header' in self._data:
            self._window.addstr(0, 1, self._interpolator.interpolate(self._data['header']), curses.A_NORMAL)
            header_offset = 1

        for index, text_line in enumerate(self._data['text']):
            self._window.addstr(header_offset + index, 1, self._interpolator.interpolate(text_line), curses.A_NORMAL)

        self._window.addstr(header_offset + len(self._data['text']), 1, self._interpolator.interpolate(self._data.get('action_name', 'Ok')), curses.A_REVERSE)

        if self._window.getch() in [curses.KEY_ENTER, ord("\n")]:
            return self._effect_resolver.resolve_effect_chain(self._data['effects'])

    def reset(self):
        pass


class _Confirm:
    def __init__(self, window, data, values, state, interpolator, effect_resolver, hotkeys):
        self._window = window
        self._data = data
        self._state = state
        self._hotkeys = hotkeys
        self._values = values
        self._interpolator = interpolator
        self._effect_resolver = effect_resolver

    def tick(self):
        self._window.addstr(0, 1,  self._interpolator.interpolate(self._data['header']), curses.A_NORMAL)

        for index, text_line in enumerate(self._data['text']):
            self._window.addstr(1 + index, 1, self._interpolator.interpolate(text_line), curses.A_NORMAL)

        for index, action in enumerate(self._data['actions']):
            mode = curses.A_REVERSE if index == self._state.lateral_position else curses.A_NORMAL
            self._window.addstr(1 + len(self._data['text']), 1 + 14 * index, self._interpolator.interpolate(action['title']), mode)

        key = self._window.getch()

        if key == curses.KEY_LEFT:
            self._state.navigate_left()
        elif key == curses.KEY_RIGHT:
            self._state.navigate_right()
        elif key in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[key])
        elif chr(key) in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[chr(key)])
        elif key in [curses.KEY_ENTER, ord("\n")]:
            return self._effect_resolver.resolve_action(self._data['actions'][self._state.lateral_position])

    def reset(self):
        self._state.reset_lateral_position()
        if 'preselected_action' not in self._data:
            return

        preselected_action = self._data['preselected_action']
        for index, action in enumerate(self._data['actions']):
            if action['title'] == preselected_action:
                self._state.lateral_position = index


class _Menu:
    def __init__(self, window, data, values, state, interpolator, effect_resolver, hotkeys):
        self._window = window
        self._data = data
        self._state = state
        self._hotkeys = hotkeys
        self._values = values
        self._interpolator = interpolator
        self._effect_resolver = effect_resolver

    def tick(self):
        self._window.addstr(0, 1,  self._interpolator.interpolate(self._data['header']), curses.A_NORMAL)

        for index, entry in enumerate(self._data['entries']):
            mode = curses.A_REVERSE if index == self._state.position else curses.A_NORMAL
            self._window.addstr(1 + index, 1,  self._interpolator.interpolate(entry['title']), mode)
            self._window.addstr(1 + index, 30,  self._interpolator.interpolate(entry.get('description', '')), mode)

        for index, action in enumerate(self._data['actions']):
            mode = curses.A_REVERSE if index == self._state.lateral_position else curses.A_NORMAL
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
        elif key in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[key])
        elif chr(key) in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[chr(key)])
        elif key in [curses.KEY_ENTER, ord("\n")]:
            return self._effect_resolver.resolve_action(self._data['actions'][self._state.lateral_position])

    def reset(self):
        self._state.reset_lateral_position()


def run_ui_engine(entrypoint: str, model: Dict[str, Any], ui_components: List[UiComponent]):
    def loader(screen):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        window = screen.subwin(0, 0)
        ui = _UiSystem(window, entrypoint, model, ui_components)
        ui.display()

    curses.wrapper(loader)

