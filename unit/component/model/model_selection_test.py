import unittest
from component.model.model_selection import update
import json

class UpdateModelSelectionTest(unittest.TestCase):
    def test_no_models(self):
        models = []
        expected_model_options = []
        actual_model_options = update(models)
        self.assertEqual(actual_model_options, expected_model_options)

    def test_model_options_returned(self):
        models = json.dumps([dict(model_name='-5 halfhours', displacement_value=5,
                           displacement_unit='halfhours'), dict(model_name='-10 hours', displacement_value=10,
                           displacement_unit='hours')])
        expected_model_options = [{'label': '-5 halfhours', 'value': '-5 halfhours'}, {'label': '-10 hours', 'value': '-10 hours'}]
        actual_model_options = update(models)
        self.assertEqual(actual_model_options, expected_model_options)