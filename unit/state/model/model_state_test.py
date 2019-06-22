import unittest
import pandas as pd
import json
from state.model.model_state import update, calculate_model_color, get_model_by_name, add_regression
from mock import patch
from datetime import datetime


class update_test(unittest.TestCase):
    model_colors = ['color1']

    def setUp(self):
        self.regression_models = {'model1': {'variables': ['Temperature'], 'correction_variable': None}, 'model2': {'variables': ['Temperature'], 'correction variable':
                                                                                                                    'Load Last Week', 'correction_variable': None}}
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Temperature': [1, 2, 3, 4, 5],
             'Load Last Week': [222, 444, 666, 888, 1110], 'Load Last Week Difference From Derived': [111, 222, 333, 444, 555]}
        self.load_data = pd.DataFrame(data=d)

    def test_initial_empty_model_list(self):
        add_displacement_timestamp = '0'
        add_regression_timestamp = '0'
        remove_model_timestamp = '0'
        displacement_value = 0
        displacement_unit = 'halfhours'
        remove_model_selection = ''
        plotted_models = []
        training_start_date = 'None'
        training_end_date = 'None'
        regression_model_choice = 'None'
        regression_model_name = ''

        expected_state = json.dumps([])
        actual_state = update(self.load_data, self.regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
                              displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
                              training_end_date, regression_model_name)
        self.assertEqual(actual_state, expected_state)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_initial_empty_model_list_add_new_displacement_model(self):
        add_displacement_timestamp = '1'
        add_regression_timestamp = '0'
        remove_model_timestamp = '0'
        displacement_value = 5
        displacement_unit = 'halfhours'
        plotted_models = json.dumps([])
        remove_model_selection = ''
        training_start_date = 'None'
        training_end_date = 'None'
        regression_model_choice = 'None'
        regression_model_name = ''

        expected_state = json.dumps([dict(model_name='-5 halfhours', model_type='displacement', model_color='color1', displacement_value=5,
                                          displacement_unit='halfhours')])
        actual_state = update(self.load_data, self.regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
                              displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
                              training_end_date, regression_model_name)
        self.assertEqual(actual_state, expected_state)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_existing_models_list_add_new_displacement_model(self):
        add_displacement_timestamp = '1'
        add_regression_timestamp = '0'
        remove_model_timestamp = '0'
        displacement_value = 10
        displacement_unit = 'hours'
        plotted_models = json.dumps([dict(model_name='-5 halfhours', model_type='displacement', model_color='color1', displacement_value=5,
                                          displacement_unit='halfhours')])
        remove_model_selection = ''
        training_start_date = 'None'
        training_end_date = 'None'
        regression_model_choice = 'None'
        regression_model_name = ''

        expected_state = json.dumps([dict(model_name='-5 halfhours',  model_type='displacement', model_color='color1', displacement_value=5,
                                          displacement_unit='halfhours'), dict(model_name='-10 hours', model_type='displacement', model_color='color1', displacement_value=10,
                                                                               displacement_unit='hours')])
        actual_state = update(self.load_data, self.regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
                              displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
                              training_end_date, regression_model_name)
        self.assertEqual(actual_state, expected_state)

    @patch('state.model.model_state.model_colors', model_colors)
    @patch('component.model.regression.regression_model.fit_to_training')
    def test_existing_models_list_add_new_regression_model(self, mock_function):
        mock_function.return_value = dict(coefficients=[111.0], intercept=0)
        add_displacement_timestamp = '0'
        add_regression_timestamp = '1'
        remove_model_timestamp = '0'
        displacement_value = 10
        displacement_unit = 'hours'
        plotted_models = json.dumps([dict(model_name='-5 halfhours', model_type='displacement', model_color='color1', displacement_value=5,
                                          displacement_unit='halfhours')])
        remove_model_selection = ''
        regression_model_choice = 'model1'
        training_start_date = '2018-01-02'
        training_end_date = '2018-01-03'
        regression_model_name = 'custom_model_name'

        expected_state = json.dumps([dict(model_name='-5 halfhours', model_type='displacement', model_color='color1', displacement_value=5,
                                          displacement_unit='halfhours'), dict(model_name='custom_model_name', model_type='regression', model_color='color1', coefficients=[111.0], intercept=0,
                                                                               x_columns=["Temperature"], corrected_column=None)])
        actual_state = update(self.load_data, self.regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
                              displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
                              training_end_date, regression_model_name)
        self.assertEqual(actual_state, expected_state)

    def test_initial_empty_model_list_remove_model(self):
        add_displacement_timestamp = '0'
        add_regression_timestamp = '0'
        remove_model_timestamp = '1'
        displacement_value = 10
        displacement_unit = 'hours'
        plotted_models = json.dumps([])
        remove_model_selection = ''
        regression_model_choice = 'None'
        training_start_date = 'None'
        training_end_date = 'None'
        regression_model_name = ''

        expected_state = json.dumps([])
        actual_state = update(self.load_data, self.regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
                              displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
                              training_end_date, regression_model_name)
        self.assertEqual(actual_state, expected_state)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_existing_models_list_remove_model(self):
        add_displacement_timestamp = '0'
        add_regression_timestamp = '0'
        remove_model_timestamp = '1'
        displacement_value = 0
        displacement_unit = 'hours'
        plotted_models = json.dumps([dict(model_name='-5 halfhours', model_type='displacement', model_color='color1', displacement_value=5,
                                          displacement_unit='halfhours'),
                                     dict(model_name='model1', model_type='regression', model_color='color2',
                                          coefficients=[111.0], intercept=0, corrected_column=None)])
        remove_model_selection = '-5 halfhours'
        regression_model_choice = 'None'
        training_start_date = 'None'
        training_end_date = 'None'
        regression_model_name = 'model1'

        expected_state = json.dumps([dict(model_name='model1', model_type='regression', model_color='color2',
                                          coefficients=[111.0], intercept=0, corrected_column=None)])
        actual_state = update(self.load_data, self.regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
                              displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
                              training_end_date, regression_model_name)
        self.assertEqual(actual_state, expected_state)


class calculate_model_color_test(unittest.TestCase):
    model_colors = ['color1', 'color2', 'color3']

    @patch('state.model.model_state.model_colors', model_colors)
    def test_no_models(self):
        plotted_models = []
        expected_color = 'color1'
        actual_color = calculate_model_color(plotted_models)
        self.assertEqual(actual_color, expected_color)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_next_color_1_model(self):
        plotted_models = [dict(model_color='color1')]
        expected_color = 'color2'
        actual_color = calculate_model_color(plotted_models)
        self.assertEqual(actual_color, expected_color)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_next_color_delete_1_model(self):
        plotted_models = [dict(model_color='color1'), dict(
            model_color='color3')]  # model with color2 has been deleted
        expected_color = 'color2'
        actual_color = calculate_model_color(plotted_models)
        self.assertEqual(actual_color, expected_color)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_next_color_delete_2_models(self):
        # model with color1 and color2 has been deleted
        plotted_models = [dict(model_color='color3')]
        expected_color = 'color1'
        actual_color = calculate_model_color(plotted_models)
        self.assertEqual(actual_color, expected_color)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_next_color_all_colors_used(self):
        plotted_models = [dict(model_color='color1'), dict(
            model_color='color2'), dict(model_color='color3')]
        expected_color = 'color1'
        actual_color = calculate_model_color(plotted_models)
        self.assertEqual(actual_color, expected_color)

    @patch('state.model.model_state.model_colors', model_colors)
    def test_next_color_all_colors_used_not_sequential(self):
        plotted_models = [dict(model_color='color2'), dict(model_color='color3'), dict(
            model_color='color1'), dict(model_color='color3')]
        expected_color = 'color2'
        actual_color = calculate_model_color(plotted_models)
        self.assertEqual(actual_color, expected_color)


class get_model_by_name_test(unittest.TestCase):
    def test_model_exists(self):
        models = [{'model_name': 'model1'}, {'model_name': 'model2'}]
        expected_output = {'model_name': 'model2'}
        output = get_model_by_name(models, 'model2')
        self.assertEqual(output, expected_output)

    def test_model_does_not_exist(self):
        models = [{'model_name': 'model1'}, {'model_name': 'model2'}]
        expected_output = None
        output = get_model_by_name(models, 'model3')
        self.assertEqual(output, expected_output)

    def test_model_empty(self):
        models = []
        expected_output = None
        output = get_model_by_name(models, 'model1')
        self.assertEqual(output, expected_output)


class AddRegression(unittest.TestCase):
    model_colors = ['color1', 'color2', 'color3']

    def setUp(self):
        self.regression_models = {'model1': {'variables': ['Temperature'], 'correction_variable': None}, 'model2': {'variables': ['Temperature'], 'correction variable':
                                                                                                                    'Load Last Week', 'correction_variable': None}}
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Temperature': [1, 2, 3, 4, 5],
             'Load Last Week': [222, 444, 666, 888, 1110], 'Load Last Week Difference From Derived': [111, 222, 333, 444, 555]}
        self.load_data = pd.DataFrame(data=d)

    @patch('state.model.model_state.model_colors', model_colors)
    @patch('component.model.regression.regression_model.fit_to_training')
    def test_add_regression_model_no_existing_models(self, mock_function):
        mock_function.return_value = dict(coefficients=[111.0], intercept=0)
        model_choice = 'model1'
        training_start_date = '2018-01-02'
        training_end_date = '2018-01-03'
        plotted_models = []
        model_name = 'model1'
        output = add_regression(self.load_data, self.regression_models,
                                plotted_models, model_choice, training_start_date, training_end_date, model_name)
        expected_output = [dict(model_name='model1', model_type='regression', model_color='color1', coefficients=[111.0], intercept=0,
                                x_columns=['Temperature'], corrected_column=None)]
        self.assertEqual(expected_output, output)

    @patch('state.model.model_state.model_colors', model_colors)
    @patch('component.model.regression.regression_model.fit_to_training')
    def test_add_regression_model_existing_models(self, mock_function):
        mock_function.return_value = dict(coefficients=[111.0], intercept=0)
        model_choice = 'model1'
        training_start_date = '2018-01-02'
        training_end_date = '2018-01-03'
        model_name = 'model1'
        plotted_models = [dict(model_name='-5 halfhours', model_type='displacement', model_color='color1', displacement_value=5,
                               displacement_unit='halfhours')]
        output = add_regression(self.load_data, self.regression_models,
                                plotted_models, model_choice, training_start_date, training_end_date, model_name)
        expected_output = [dict(model_name='-5 halfhours', model_type='displacement', model_color='color1', displacement_value=5,
                                displacement_unit='halfhours'), dict(model_name='model1', model_type='regression', model_color='color2',
                                                                     coefficients=[111.0], intercept=0, x_columns=['Temperature'], corrected_column=None)]
        self.assertEqual(expected_output, output)
