import unittest
from component.model.regression.regression_training_data_date_picker_day_range import update_date
from mock import patch


class UpdateDateTest(unittest.TestCase):
    regression_models = {'Test Model': {'variables': ['Temperature Last Day', 'Wind Speed Difference Last Day'],
                                        'correction_variable': 'Load Last Day', 'description': 'ABC123', 'training': {'start_date': '1970-01-01', 
                                        'end_date': '1970-01-02'}},
                         'Test Model 2': {'variables': ['Humidity Difference Last Day'], 'correction_variable': None, 'description': '', 'training': {}}}
    
    @patch('component.model.regression.regression_training_data_date_picker_day_range.regression_models', regression_models)
    def test_return_start_date(self):
        model_selection = 'Test Model'
        previous_start_date = '1980-01-01'
        expected_output = '1970-01-01'
        actual_output = update_date(model_selection, previous_start_date, 'start_date')
        self.assertEqual(actual_output, expected_output)

    @patch('component.model.regression.regression_training_data_date_picker_day_range.regression_models', regression_models)
    def test_model_selection_none_return_previous_end_date(self):
        model_selection = 'None'
        previous_end_date = '1980-01-01'
        expected_output = '1980-01-01'
        actual_output = update_date(model_selection, previous_end_date, 'end_date')
        self.assertEqual(actual_output, expected_output)

    @patch('component.model.regression.regression_training_data_date_picker_day_range.regression_models', regression_models)
    def test_training_empty_return_previous_start_date(self):
        model_selection = 'Test Model 2'
        previous_start_date = '1980-01-01'
        expected_output = '1980-01-01'
        actual_output = update_date(model_selection, previous_start_date, 'start_date')
        self.assertEqual(actual_output, expected_output)
