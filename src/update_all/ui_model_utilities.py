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

def gather_default_values(model):
    result = {}
    if 'variables' in model:
        _add_variables_default_values(result, model['variables'])
    if 'items' in model:
        for item in model['items'].values():
            if 'variables' in item:
                _add_variables_default_values(result, item['variables'])

    return result


def _add_variables_default_values(result, variables):
    for variable, description in variables.items():
        default_value = description['default']
        if default_value == 'true':
            default_value = True
        elif default_value == 'false':
            default_value = False
        elif default_value.isdigit():
            default_value = int(default_value)
        result[variable] = default_value


def list_variables_with_group(model, group):
    group = group.lower()
    result = {}
    if 'variables' in model:
        _add_variables_renames_with_group(result, model['variables'], group)
    if 'items' in model:
        for item in model['items'].values():
            if 'variables' in item:
                _add_variables_renames_with_group(result, item['variables'], group)

    return result


def _add_variables_renames_with_group(result, variable_descriptions, group):
    for variable, description in variable_descriptions.items():
        if 'group' in description and description['group'].lower() == group:
            result[variable] = description['rename'] if 'rename' in description else variable


def dynamic_convert_string(value):
    if type(value) == str:
        if value == 'true':
            value = True
        elif value == 'false':
            value = False
        elif value.isdigit():
            value = int(value)

    return value
