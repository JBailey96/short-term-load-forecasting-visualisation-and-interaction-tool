import unittest
import pandas as pd
from datetime import datetime
from numpy.testing import assert_array_equal
from component.graph.visualise_model.load_graph import update, calculate_style, calculate_x_axis_layout

class update_load_graph_test(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555]}
        self.load_data = pd.DataFrame(data=d)

    def test_load_graph_returned_no_model(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        highlight_variable = 'None'
        highlight_value = None
        characteristics_y_axis_selection = 'None'
        models = []
        output = update(self.load_data, start_date, end_date, models, characteristics_y_axis_selection, highlight_variable,
         highlight_value)
        self.assertEqual(len(output[0].figure['data']), 1)

    def test_load_graph_returned_model(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        characteristics_y_axis_selection = 'None'
        models = [dict(model_name='model 1', model_type='displacement', model_color='red', displacement_value=48,
                           displacement_unit='Half Hours')]
        highlight_variable = 'None'
        highlight_value = None
        output = update(self.load_data, start_date, end_date, models, characteristics_y_axis_selection, highlight_variable,
        highlight_value)
        self.assertEqual(len(output[0].figure['data']), 2)


class calculate_style_load_graph_test(unittest.TestCase):
    def test_model_plotted_and_characteristics_graph_visible(self):
        is_displacement = ['True']
        characteristics_y_axis_selection = 'Not None'
        expected_style = {'height': '30vh', 'width': '98vw'}
        actual_style = calculate_style(
            is_displacement, characteristics_y_axis_selection)
        self.assertEqual(actual_style, expected_style)

    def test_model_not_plotted_and_characteristics_graph_visible(self):
        is_displacement = []
        characteristics_y_axis_selection = 'Not None'
        expected_style = {'height': '40vh', 'width': '98vw'}
        actual_style = calculate_style(
            is_displacement, characteristics_y_axis_selection)
        self.assertEqual(actual_style, expected_style)

    def test_model_not_plotted_and_characteristics_graph_not_visible(self):
        is_displacement = []
        characteristics_y_axis_selection = 'None'
        expected_style = {'height': '80vh', 'width': '98vw'}
        actual_style = calculate_style(
            is_displacement, characteristics_y_axis_selection)
        self.assertEqual(actual_style, expected_style)

    def test_model_plotted_and_characteristics_graph_not_visible(self):
        is_displacement = ['True']
        characteristics_y_axis_selection = 'None'
        expected_style = {'height': '60vh', 'width': '98vw'}
        actual_style = calculate_style(
            is_displacement, characteristics_y_axis_selection)
        self.assertEqual(actual_style, expected_style)


class calculate_x_axis_layout_test(unittest.TestCase):
    def test_y_axis_selected(self):
        characteristics_y_axis_selection = 'Not None'
        expected_style = dict(showticklabels=False)
        actual_style = calculate_x_axis_layout(
            characteristics_y_axis_selection)
        self.assertEqual(actual_style, expected_style)

    def test_y_axis_not_selected(self):
        characteristics_y_axis_selection = 'None'
        expected_style = dict(
            title='Date', tickformat='%a %Y-%m-%d %H:%M', automargin=True)
        actual_style = calculate_x_axis_layout(
            characteristics_y_axis_selection)
        self.assertEqual(actual_style, expected_style)