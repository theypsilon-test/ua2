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
import copy
from typing import Dict, Any, List, Tuple

from update_all.ui_engine import expand_type


def basic_types(): return 'menu', 'confirm', 'message'
def special_navigate_targets(): return 'back', 'abort', 'exit_and_run'


def all_nodes(model: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    return list_nodes_in_model(expand_model_types(model))


def expand_model_types(model: Dict[str, Any]) -> Dict[str, Any]:
    model = copy.deepcopy(model)
    for _, node in list_nodes_in_model(model):
        expand_type(node, model)
    return model


def list_nodes_in_model(model: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    result = []
    for key, item in model['items'].items():
        result.extend(list_nodes(key, item))
    return result


def list_nodes(key, item) -> List[Tuple[str, Dict[str, Any]]]:
    result = [(key, item)]
    result.extend(list_hotkeys_nodes(key, item))
    result.extend(list_action_nodes(key, item))
    result.extend(list_entries_nodes(key, item))
    result.extend(list_effects_nodes(key, item))
    return result


def list_hotkeys_nodes(key, node):
    if 'hotkeys' not in node:
        return []
    result = []
    for i_hk, hotkey in enumerate(node['hotkeys']):
        result.extend(list_actions(f'{key}.hotkeys[{i_hk}]', hotkey['action']))
    return result


def list_action_nodes(key, node):
    if 'actions' not in node:
        return []

    result = []
    for i_a, action in enumerate(node['actions']):
        if action['type'] == 'fixed':
            result.extend(list_actions(f'{key}.actions[{i_a}].fixed', action['fixed']))
    return result


def list_entries_nodes(key, node):
    if 'entries' not in node:
        return []

    result = []
    for i_e, entry in enumerate(node['entries']):
        if 'actions' in entry:
            for symbol, action in entry['actions'].items():
                result.extend(list_actions(f'{key}.entries[{i_e}].actions[{symbol}]', action))
    return result


def list_effects_nodes(key, node):
    result = []
    if 'effects' in node:
        result.extend(list_actions(f'{key}.effects', node['effects']))
    return result


def list_actions(key, actions) -> List[Tuple[str, Dict[str, Any]]]:
    result = []
    for i_a, action in enumerate(actions):
        if action['type'] in basic_types():
            result.extend(list_nodes(f'{key}.action[{i_a}]', action))
        elif action['type'] == 'condition':
            result.extend(list_actions(f'{key}.action[{i_a}].true', action['true']))
            result.extend(list_actions(f'{key}.action[{i_a}].false', action['false']))
        else:
            result.append((f'{key}.{action["type"]}', action))

    return result


def all_navigate_nodes(model) -> List[Tuple[str, Dict[str, Any]]]:
    return [(key, node) for key, node in all_nodes(model) if node['type'] == 'navigate']


def all_nodes_of_type(model, *args) -> List[Tuple[str, Dict[str, Any]]]:
    return [(key, node) for key, node in all_nodes(model) if node['type'] in [*args]]