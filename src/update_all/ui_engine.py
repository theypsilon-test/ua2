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
from typing import Dict, Callable, List, Any, Union, Optional


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


class Interpolator(abc.ABC):
    def interpolate(self, text: str) -> str:
        """Interpolates any value inside a string into another string according to the formatters"""


class Action:
    def __init__(self, props, selection):
        self.props = props
        self.selection = selection


class EffectChain:
    def __init__(self, chain):
        self.chain = chain


class UiSection(abc.ABC):
    def process_key(self) -> Optional[Union[int, EffectChain, Action]]:
        """Writes text on window, reads char and returns it"""

    def reset(self) -> None:
        """Resets the UI Section"""


class UiSectionFactory(abc.ABC):
    def create_ui_section(self, ui_type: str, window: curses.window, data: Dict[str, Any], interpolator: Interpolator) -> UiSection:
        """Creates an instance of a UiSection"""


class _UiSystem(Ui):
    def __init__(self, window, entrypoint, model, ui_components, ui_section_factory: UiSectionFactory):
        self._window = window
        self._section = entrypoint
        self._model = model
        self._ui_components = ui_components
        self._ui_section_factory = ui_section_factory
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
            new_section = self._current_section_state().process()

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
        expand_ui_type(data, model)

        data['formatters'] = {**data.get('formatters', {}), **model.get('formatters', {})}
        data['variables'] = {**data.get('variables', {}), **model.get('variables', {})}

        interpolator = _Interpolator(data, values)
        effect_resolver = _EffectResolver(self, data, values)
        for component in ui_components:
            effect_resolver.add_ui_component(component)

        hotkeys = {}
        for hk in data.get('hotkeys', []):
            for key in hk['keys']:
                hotkeys[key] = hk['action']

        ui_type = data['ui'] if 'ui' in data else None
        if ui_type is None:
            raise ValueError(f'Wrong ui_type: "{data["ui"] if "ui" in data else "`ui` field not found"}"')

        ui_section = self._ui_section_factory.create_ui_section(ui_type, window, data, interpolator)
        return _UiSectionProcessor(ui_section, effect_resolver, hotkeys)


class _UiSectionProcessor:
    def __init__(self, ui_section: UiSection, effect_resolver, hotkeys):
        self._ui_section = ui_section
        self._effect_resolver = effect_resolver
        self._hotkeys = hotkeys

    def process(self):
        key_result = self._ui_section.process_key()

        if isinstance(key_result, Action):
            return self._effect_resolver.resolve_action(key_result)
        elif isinstance(key_result, EffectChain):
            return self._effect_resolver.resolve_effect_chain(key_result.chain)
        elif key_result in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[key_result])
        elif chr(key_result) in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[chr(key_result)])
        elif not isinstance(key_result, int):
            raise TypeError(f'Result with type {str(type(key_result))} can not be processed by the effect resolver')

    def reset(self):
        self._ui_section.reset()


def expand_ui_type(data, model):
    while data['ui'] in model['base_types']:
        base_type = model['base_types'][data['ui']]
        if 'ui' not in base_type:
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


class _Interpolator(Interpolator):
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
    def __init__(self, ui, data, values):
        self._ui = ui
        self._data = data
        self._values = values
        self._additional_effects = {}

    def add_ui_component(self, ui_component):
        ui_component.initialize_effects(self._ui, self._additional_effects)

    def resolve_effect_chain(self, chain):
        result = None
        for effect in chain:
            if 'ui' in effect:
                return effect
            elif 'type' not in effect:
                raise ValueError('Effects should either have property `ui` or property `type`.')
            elif effect['type'] == 'condition':
                variable = effect['variable']
                return self.resolve_effect_chain(effect[self._values[variable]])
            elif effect['type'] == 'navigate':
                return effect['target']
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
            elif effect['type'] in self._additional_effects:
                self._additional_effects[effect['type']](effect)
            else:
                raise NotImplementedError(f'Wrong effect type :"{effect["type"]}"')

        return result

    def resolve_action(self, action: Action):
        if action.props['type'] == 'symbol':
            if 'actions' not in action.selection:
                raise ValueError('Selection does not contain nested actions that can be linked to symbol.')
            return self.resolve_effect_chain(action.selection['actions'][action.props['symbol']])
        elif action.props['type'] == 'fixed':
            return self.resolve_effect_chain(action.props['fixed'])
        else:
            raise NotImplementedError(f'Wrong action type :"{action.props["type"]}"')


def run_ui_engine(entrypoint: str, model: Dict[str, Any], ui_components: List[UiComponent], ui_section_factory: UiSectionFactory):
    def loader(screen):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        window = screen.subwin(0, 0)
        ui = _UiSystem(window, entrypoint, model, ui_components, ui_section_factory)
        ui.display()

    curses.wrapper(loader)

