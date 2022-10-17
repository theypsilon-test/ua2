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
from typing import Set


def gather_variable_declarations(model, group = None):
    group = {} if group is None else {group}
    result = {}
    if 'variables' in model:
        _add_variables_default_values(result, model['variables'], group)
    if 'items' in model:
        for item in model['items'].values():
            if 'variables' in item:
                _add_variables_default_values(result, item['variables'], group)

    return result


def _add_variables_default_values(result, variables, group):
    for variable, description in variables.items():
        if len(group) > 0:
            if 'group' not in description:
                continue
            description_group = description['group'] if isinstance(description['group'], list) else [description['group']]
            if group.isdisjoint(description_group):
                continue

        result[variable] = description


def gather_target_variables(model) -> Set[str]:
    result = set()
    if 'items' in model:
        for item in model['items'].values():
            _add_target_variables(result, item)
    return result


def _add_target_variables(result: Set[str], item) -> None:
    if 'actions' in item:
        if isinstance(item['actions'], dict):
            for action_chain in item['actions'].values():
                for action in action_chain:
                    _add_target_variables(result, action)

        elif isinstance(item['actions'], list):
            for action in item['actions']:
                _add_target_variables(result, action)

    if 'entries' in item:
        for entry in item['entries']:
            _add_target_variables(result, entry)

    if 'effects' in item:
        for effect in item['effects']:
            _add_target_variables(result, effect)

    if 'header' in item:
        result.update(_extract_variables_from_text(item['header']))

    if 'type' not in item:
        return

    node_type = item['type']
    if node_type == 'fixed':
        for fixed in item['fixed']:
            _add_target_variables(result, fixed)

    elif node_type == 'rotate_variable':
        result.add(item['target'])

    elif node_type == 'condition':
        result.add(item['variable'])

        for true in item['true']:
            _add_target_variables(result, true)

        for false in item['false']:
            _add_target_variables(result, false)


def _extract_variables_from_text(text: str) -> Set[str]:
    result = set()

    reading_state = 0
    reading_value = ''
    for character in text:
        if reading_state == 0:
            if character == '{':
                reading_state = 1
                reading_value = ''

        elif reading_state == 1:
            if character == ':':
                reading_state = 2
                result.add(reading_value)
            elif character == '}':
                reading_state = 0
                result.add(reading_value)
            else:
                reading_value += character

        if reading_state == 2:
            if character == '}':
                reading_state = 0
                result.add(reading_value)

    return result


def dynamic_convert_string(value):
    if type(value) == str:
        lower_value = value.lower()
        if lower_value == 'true':
            value = True
        elif lower_value == 'false':
            value = False
        elif value.isdigit():
            value = int(value)

    return value
