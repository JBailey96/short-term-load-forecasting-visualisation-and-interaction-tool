import unittest
from component.model.regression.regression_model_name_input import set_default_model_name

class SetDefaultModelNameTest(unittest.TestCase):
    def test_return_model_name(self):
        model_selection = 'model123'
        expected_output = 'model123'
        actual_output = set_default_model_name(model_selection)
        self.assertEqual(actual_output, expected_output)
    
    def test_return_empty_model_name(self):
        model_selection = 'None'
        expected_output = ''
        actual_output = set_default_model_name(model_selection)
        self.assertEqual(actual_output, expected_output)