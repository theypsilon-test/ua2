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
from typing import Dict, Callable, List, Any, Union, Optional, Tuple

from update_all.ui_model_utilities import gather_variable_declarations


class Ui(abc.ABC):
    def get_value(self, key: str) -> str:
        """Gets value for variable on the given key"""

    def set_value(self, key: str, value: Any) -> None:
        """Sets value as string for variable on the given key"""


class UiComponent(abc.ABC):
    def initialize_effects(self, ui: Ui, effects: Dict[str, Callable[[], None]]):
        """Initializes the effects dictionary if necessary"""


class Interpolator(abc.ABC):
    def interpolate(self, text: str) -> str:
        """Interpolates any value inside a string into another string according to the formatters"""


class EffectChain:
    def __init__(self, chain):
        self.chain = chain


ProcessKeyResult = Union[int, EffectChain]


class UiSection(abc.ABC):
    def process_key(self) -> Optional[ProcessKeyResult]:
        """Writes text on window, reads char and returns it"""

    def reset(self) -> None:
        """Resets the UI Section"""

    def clear(self) -> None:
        """Clears the UI Section"""

class UiSectionFactory(abc.ABC):
    def create_ui_section(self, ui_type: str, data: Dict[str, Any], interpolator: Interpolator) -> UiSection:
        """Creates an instance of a UiSection"""


class UiApplication(abc.ABC):
    def initialize_ui(self, ui: Ui, screen: curses.window) -> Tuple[List[UiComponent], UiSectionFactory]:
        """Initializes the theme at the start"""


def run_ui_engine(entrypoint: str, model: Dict[str, Any], ui_application: UiApplication):
    def loader(screen):
        ui = _UiSystem(screen, entrypoint, model, ui_application)
        ui.execute()

    curses.wrapper(loader)


class _UiSystem(Ui):
    def __init__(self, screen, entrypoint, model, ui_application: UiApplication):
        self._screen = screen
        self._entrypoint = entrypoint
        self._model = model
        self._ui_application = ui_application
        self._values = {}

    def get_value(self, key: str) -> str:
        return self._values[key]

    def set_value(self, key: str, value: Any) -> None:
        self._values[key] = value

    def execute(self):
        self._values.update({k: v['default'] for k, v in gather_variable_declarations(self._model).items()})

        ui_components, ui_section_factory = self._ui_application.initialize_ui(self, self._screen)

        runtime = _UiRuntime(self._model, self._entrypoint, self, ui_components, ui_section_factory)
        runtime.run()


class _UiRuntime:
    def __init__(self, model, entrypoint, ui: Ui, ui_components: List[UiComponent], ui_section_factory: UiSectionFactory):
        self._model = model
        self._section = entrypoint
        self._items = self._model['items']
        self._section_states = {}
        self._history = []
        self._ui = ui
        self._ui_components = ui_components
        self._ui_section_factory = ui_section_factory

    def run(self):
        self._current_section_state().reset()

        while True:
            new_section = self._current_section_state().process()

            curses.doupdate()

            if new_section is None:
                continue

            if new_section == 'exit_and_run':
                break
            elif new_section == 'abort':
                exit(0)
            elif new_section == 'back':
                if len(self._history) == 0:
                    break
                self._section = self._history.pop()

            elif new_section == 'clear_window':
                self._current_section_state().clear()
                continue
            elif isinstance(new_section, dict):
                self._push_history()
                self._section = '@temporary'
                self._section_states['@temporary'] = self._make_section_state(new_section)
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
            self._section_states[self._section] = self._make_section_state(self._items[self._section])
        return self._section_states[self._section]

    def _make_section_state(self, data):
        expand_ui_type(data, self._model)

        for field in ['formatters', 'variables']:
            data[field] = data.get(field, {})
            data[field].update(self._model.get(field, {}))
            for section in self._history:
                data[field].update(self._items[section].get(field, {}))

        hotkeys = {}
        for hk in data.get('hotkeys', []):
            for key in hk['keys']:
                hotkeys[key] = hk['action']

        interpolator = _Interpolator(data, self._ui)
        effect_resolver = _EffectResolver(self._ui, data)
        for component in self._ui_components:
            effect_resolver.add_ui_component(component)

        ui_type = data['ui'] if 'ui' in data else None
        if ui_type is None:
            raise ValueError(f'Wrong ui_type: "{data["ui"] if "ui" in data else "`ui` field not found"}"')

        ui_section = self._ui_section_factory.create_ui_section(ui_type, data, interpolator)
        return _UiSectionProcessor(ui_section, effect_resolver, hotkeys)


class _UiSectionProcessor:
    def __init__(self, ui_section: UiSection, effect_resolver, hotkeys):
        self._ui_section = ui_section
        self._effect_resolver = effect_resolver
        self._hotkeys = hotkeys

    def process(self):
        key_result = self._ui_section.process_key()

        if isinstance(key_result, EffectChain):
            return self._effect_resolver.resolve_effect_chain(key_result.chain)
        elif key_result in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[key_result])
        elif chr(key_result) in self._hotkeys:
            return self._effect_resolver.resolve_effect_chain(self._hotkeys[chr(key_result)])
        elif not isinstance(key_result, int):
            raise TypeError(f'Result with type {str(type(key_result))} can not be processed by the effect resolver')

    def reset(self):
        self._ui_section.reset()

    def clear(self):
        self._ui_section.clear()


def expand_ui_type(data, model):
    data['type'] = 'ui'
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
    def __init__(self, data, ui: Ui):
        self._data = data
        self._ui = ui

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
                        values[reading_value] = variable_type[self._ui.get_value(reading_value)]
                    else:
                        values[reading_value] = self._ui.get_value(reading_value)
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
                        values[reading_value + ':bool'] = 'true' if bool(self._ui.get_value(reading_value)) else 'false'
                    elif reading_modifier in self._data['formatters']:
                        variable_type = self._data['formatters'][reading_modifier]
                        try:
                            values[reading_value + ':' + reading_modifier] = variable_type[self._ui.get_value(reading_value)]
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
                        values[reading_value + ':' + reading_modifier + '=' + ','.join(reading_arguments)] = variable_type[self._ui.get_value(reading_value)].format(*reading_arguments)
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
    def __init__(self, ui, data):
        self._ui = ui
        self._data = data
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
                return self.resolve_effect_chain(effect[self._ui.get_value(variable)])
            elif effect['type'] == 'navigate':
                return effect['target']
            elif effect['type'] == 'rotate_variable':
                target_variable = effect['target']
                possible_values = self._data['variables'][target_variable]['values']

                cur_index = 0
                for index, var_value in enumerate(possible_values):
                    if var_value == self._ui.get_value(target_variable):
                        cur_index = index
                        break

                cur_index += 1
                if cur_index >= len(possible_values):
                    cur_index = 0

                if possible_values[cur_index] != self._ui.get_value(target_variable):
                    self._ui.set_value(target_variable, possible_values[cur_index])
                    result = 'clear_window'
            elif effect['type'] in self._additional_effects:
                self._additional_effects[effect['type']](effect)
            else:
                raise NotImplementedError(f'Wrong effect type :"{effect["type"]}"')

        return result
