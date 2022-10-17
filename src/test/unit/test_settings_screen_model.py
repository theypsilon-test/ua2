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
import unittest

from test.ui_model_test_utils import special_navigate_targets, all_nodes_of_type
from update_all.config_reader import Config
from update_all.databases import model_variables_by_db_id, db_ids_by_model_variables
from update_all.settings_screen_model import settings_screen_model
from update_all.ui_model_utilities import gather_variable_declarations, \
    dynamic_convert_string, gather_target_variables


class TestSettingsScreenModel(unittest.TestCase):

    def setUp(self) -> None:
        self.model = settings_screen_model()

    def test___there_are_some_navigate_nodes(self):
        nodes = all_nodes_of_type(self.model, 'navigate')
        self.assertGreater(len(nodes), len(self.model['items']))

    def test_all_navigate_nodes___have_no_invalid_targets(self):
        navigate_nodes = all_nodes_of_type(self.model, 'navigate')
        invalid_target_nodes = [(key, node) for key, node in navigate_nodes if node['target'] not in self.model['items'] and node['target'] not in special_navigate_targets()]

        self.assertEqual([], invalid_target_nodes)

    def test_main_variables___have_length_greater_than_5(self):
        self.assertGreater(len(gather_variable_declarations(self.model, "ua_ini")), 5)

    def test_ao_variables___have_length_greater_than_5(self):
        self.assertGreater(len(gather_variable_declarations(self.model, "ao_ini")), 5)

    def test_ao_variables___all_start_with_arcade_organizer_prefix(self):
        prefix = "arcade_organizer_"
        for variable in gather_variable_declarations(self.model, "ao_ini"):
            self.assertEqual(prefix, variable[0:len(prefix)])

    def test_config_default_values___match_main_variables_default_values(self):
        config = Config()

        main_variables = gather_variable_declarations(self.model, "ua_ini")

        default_config_values = {variable: getattr(config, variable) for variable in main_variables if hasattr(config, variable)}
        for db_id, variable in model_variables_by_db_id().items():
            default_config_values[variable] = db_id in config.databases

        default_model_main_values = {variable: dynamic_convert_string(description['default']) for variable, description in main_variables.items()}

        self.assertNotEqual({}, default_config_values)
        self.assertNotEqual({}, default_model_main_values)
        self.assertEqual(default_config_values, default_model_main_values)

    def test_all_database_variables_are_declared_in_the_model(self):
        db_variables = set(db_ids_by_model_variables())
        model_variables = set(gather_variable_declarations(self.model, 'db'))

        self.assertGreaterEqual(len(db_variables), 5)
        self.assertSetEqual(db_variables, model_variables)

    def test_target_variables_are_declared_in_the_model(self):
        target_variables = gather_target_variables(self.model)
        declared_variables = set(gather_variable_declarations(self.model))

        self.assertGreaterEqual(len(target_variables), 5)
        self.assertSetEqual(target_variables, declared_variables)
