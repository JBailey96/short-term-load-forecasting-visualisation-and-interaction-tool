import unittest
from component.graph.visualise_model.characteristics_graph import update, calculate_style
from datetime import datetime
import pandas as pd


class calculate_style_characteristics_graph_test(unittest.TestCase):
    def test_model_plotted(self):
        is_displacement = ['True']
        expected_style = dict(height='30vh', width='98vw')
        actual_style = calculate_style(is_displacement)
        self.assertEqual(actual_style, expected_style)

    def test_model_not_plotted(self):
        is_displacement = []
        expected_style = dict(height='40vh', width='98vw')
        actual_style = calculate_style(is_displacement)
        self.assertEqual(actual_style, expected_style)


class update_characteristics_graph_test(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555]}
        self.load_data = pd.DataFrame(data=d)

    def test_no_y_axis_selection(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        characteristics_y_axis_selection = 'None'
        models = []
        highlighted_variable = 'None'
        highlighted_value = None
        children = update(
            self.load_data, start_date, end_date, models, characteristics_y_axis_selection, highlighted_variable, highlighted_value)
        self.assertEqual(len(children), 0)

    def test_y_axis_selection_no_displacement_model(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        characteristics_y_axis_selection = 'Date'
        models = []
        highlighted_variable = 'None'
        highlighted_value = None
        output = update(
            self.load_data, start_date, end_date, models, characteristics_y_axis_selection, highlighted_variable, highlighted_value)
        self.assertEqual(len(output[0].figure['data']), 1)

    def test_y_axis_selection_with_displacement_model(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        characteristics_y_axis_selection = 'Date'
        models = [dict(model_name='model 1', model_type='displacement', model_color='red', displacement_value=48,
                       displacement_unit='Half Hours')]
        highlighted_variable = 'None'
        highlighted_value = None
        output = update(
            self.load_data, start_date, end_date, models, characteristics_y_axis_selection, highlighted_variable, highlighted_value)
        self.assertEqual(len(output[0].figure['data']), 2)

    def test_y_axis_selection_with_regression_model(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        characteristics_y_axis_selection = 'Date'
        models = [dict(model_name='model 1', model_type='regression', model_color='red', coefficients=[111.0], intercept=0,
                       x_columns=["Temperature"], corrected_column=None)]
        highlighted_variable = 'None'
        highlighted_value = None
        output = update(
            self.load_data, start_date, end_date, models, characteristics_y_axis_selection, highlighted_variable, highlighted_value)
        self.assertEqual(len(output[0].figure['data']), 1)

    def test_y_axis_selection_with_displacement_model_and_regression_model(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        characteristics_y_axis_selection = 'Date'
        models = [dict(model_name='model 1', model_type='displacement', model_color='red', displacement_value=48,
                       displacement_unit='Half Hours'), dict(model_name='model 2', model_type='regression', model_color='red', coefficients=[111.0], intercept=0,
                                                             x_columns=["Temperature"], corrected_column=None)]
        highlighted_variable = 'None'
        highlighted_value = None
        output = update(
            self.load_data, start_date, end_date, models, characteristics_y_axis_selection, highlighted_variable, highlighted_value)
        self.assertEqual(len(output[0].figure['data']), 2)
        self.assertEqual(output[0].figure['data'][0]['name'], 'Actual Load')
        self.assertEqual(output[0].figure['data'][1]['name'], 'model 1')

