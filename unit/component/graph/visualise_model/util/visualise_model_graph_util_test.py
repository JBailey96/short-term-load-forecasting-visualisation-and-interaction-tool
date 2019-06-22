import unittest
import pandas as pd
from datetime import datetime
from numpy.testing import assert_array_equal
from component.graph.visualise_model.util.visualise_model_graph_util import add_visualised_graph
import numpy as np
from mock import patch

class add_visualised_graph_test(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 4, 0), datetime(2018, 1, 5, 0)], 'Load': [111, 222, 333, 444, 555], 'Holiday': ['Holiday', 'Holiday', 'Holiday', 'Non-Holiday',
                      'Holiday'], 'Is_Weekend': [True, True, False, False, True], 'Day': [5, 4, 3, 2, 1]}
        self.load_data = pd.DataFrame(data=d)

    def test_return_multiple_date_range(self):
        start_date = datetime(2018, 1, 1)
        end_date = datetime(2018, 1, 2)
        output = add_visualised_graph(self.load_data, start_date, end_date)
        assert_array_equal(output['data'][0]['x'], [datetime(
            2018, 1, 1, 0), datetime(2018, 1, 2, 0)])
        self.assertEqual(output['data'][0]['name'], 'Actual Load')


    def test_return_single_date_range(self):
        start_date = datetime(2018, 1, 1)
        end_date = datetime(2018, 1, 1)
        output = add_visualised_graph(self.load_data, start_date, end_date)
        assert_array_equal(output['data'][0]['x'], [datetime(2018, 1, 1, 0)])

    def test_return_no_date_range(self):
        start_date = datetime(2019, 1, 1)
        end_date = datetime(2019, 1, 1)
        output = add_visualised_graph(self.load_data, start_date, end_date)
        assert_array_equal(output['data'][0]['x'], [])

    def test_return_no_date_range_start_after_end(self):
        start_date = datetime(2019, 1, 1)
        end_date = datetime(2018, 1, 1)
        output = add_visualised_graph(self.load_data, start_date, end_date)
        assert_array_equal(output['data'][0]['x'], [])

    def test_return_all_date_range(self):
        start_date = datetime(1999, 1, 1)
        end_date = datetime(2019, 1, 1)
        output = add_visualised_graph(self.load_data, start_date, end_date)
        assert_array_equal(output['data'][0]['x'], [datetime(2018, 1, 1, 0), datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0), datetime(2018, 1, 4, 0), datetime(2018, 1, 5, 0)])

    def test_return_highlighted_holidays(self):
        start_date = datetime(1999, 1, 1)
        end_date = datetime(2019, 1, 1)
        highlight_variable = 'Holiday'
        highlight_value = 'All'
        output = add_visualised_graph(self.load_data, start_date, end_date, highlight_variable=highlight_variable, highlight_value=highlight_value)
        assert_array_equal(output['data'][0]['x'], [datetime(2018, 1, 1, 0), datetime(
            2018, 1, 2, 0), datetime(2018, 1,3, 0), datetime(2018, 1, 4, 0), datetime(2018, 1, 5, 0)])
        # assert_array_equal(output['data'][1]['x'], [datetime(2018, 1, 1, 0), datetime(
        #     2018, 1, 1, 1), datetime(2018, 1, 2, 0), NaT, datetime(2018, 1, 4, 0)])
        # Pandas internal NAT type does not work with assert_array_equal
        self.assertEqual(len(output['data'][1]['x']), 5)
        self.assertEqual(output['data'][1]['x'][0], datetime(2018, 1, 1, 0))
        self.assertEqual(output['data'][1]['x'][1], datetime(2018, 1, 2, 0))
        self.assertEqual(output['data'][1]['x'][2], datetime(2018, 1, 3, 0))
        self.assertIsInstance(output['data'][1]['x'][3], pd._libs.tslibs.nattype.NaTType)
        self.assertEqual(output['data'][1]['x'][4], datetime(2018, 1, 5, 0))
        assert_array_equal(output['data'][1]['y'], [111., 222., 333., None, 555])
        self.assertEqual(output['data'][1]['name'], 'Highlighted Load')
        self.assertEqual(output['data'][1]['marker']['color'], 'red')
        self.assertEqual(output['data'][1]['line']['width'], 2)

    def test_return_highlighted_weekends(self):
        start_date = datetime(1999, 1, 1)
        end_date = datetime(2019, 1, 1)
        highlight_variable = 'Day'
        highlight_value = 'Weekend'
        output = add_visualised_graph(self.load_data, start_date, end_date, highlight_variable=highlight_variable, highlight_value=highlight_value)
        assert_array_equal(output['data'][1]['y'], [111., 222., None, None, 555])

    def test_return_highlighted_workdays(self):
        start_date = datetime(1999, 1, 1)
        end_date = datetime(2019, 1, 1)
        highlight_variable = 'Day'
        highlight_value = 'Workday'
        output = add_visualised_graph(self.load_data, start_date, end_date, highlight_variable=highlight_variable, highlight_value=highlight_value)
        assert_array_equal(output['data'][1]['y'], [None, None, 333., 444., None])
    
    def test_return_highlighted_day(self):
        start_date = datetime(1999, 1, 1)
        end_date = datetime(2019, 1, 1)
        highlight_variable = 'Day'
        highlight_value = 5
        output = add_visualised_graph(self.load_data, start_date, end_date, highlight_variable=highlight_variable, highlight_value=highlight_value)
        assert_array_equal(output['data'][1]['y'], [111., None, None, None, None])

    def test_return_ranged_and_displaced_by_day(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        models = [dict(model_name='model 1', model_type='displacement', displacement_value=48, model_color='red',
                           displacement_unit='Half Hours')]
        output = add_visualised_graph(
            self.load_data, start_date, end_date, models, {})
        assert_array_equal(output['data'][0]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0)])
        assert_array_equal(output['data'][0]['y'], [222, 333])
        assert_array_equal(output['data'][1]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0)])
        assert_array_equal(output['data'][1]['y'], [111, 222])
        self.assertEqual(len(output['data']), 2)

    @patch('component.graph.visualise_model.util.visualise_model_graph_util.regression_model.predict')
    def test_return_ranged_and_regression_model(self, mock_function):
        mock_function.return_value = [333, 444]
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        models = [dict(model_name='model1', model_type='regression', model_color='red', coefficients=[111.0], intercept=0,
                                                                               x_columns=["Temperature"], corrected_column=None)]
        output = add_visualised_graph(
            self.load_data, start_date, end_date, models, {})
        assert_array_equal(output['data'][0]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0)])
        assert_array_equal(output['data'][0]['y'], [222, 333])
        assert_array_equal(output['data'][1]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0)])
        assert_array_equal(output['data'][1]['y'], [333, 444])
        self.assertEqual(len(output['data']), 2)

    @patch('component.graph.visualise_model.util.visualise_model_graph_util.regression_model.predict')
    def test_return_ranged_and_regression_error(self, mock_function):
        mock_function.side_effect = Exception()
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        models = [dict(model_name='model1', model_type='regression', model_color='red', coefficients=[111.0], intercept=0,
                                                                               x_columns=["Temperature Last Week"], corrected_column=None)]
        output = add_visualised_graph(
            self.load_data, start_date, end_date, models, {})
        assert_array_equal(output['data'][0]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0)])
        assert_array_equal(output['data'][0]['y'], [222, 333])
        self.assertEqual(len(output['data']), 1)

    def test_return_ranged_and_1_displaced_model_out_of_range_and_1_in_range(self):
        start_date = '2018-01-02'
        end_date = '2018-01-04'
        models = [dict(model_name='model 1', model_type='displacement', model_color='red', displacement_value=96,
                           displacement_unit='Half Hours'), dict(model_name='model 2', model_type='displacement', model_color='red', displacement_value=48,
                           displacement_unit='Half Hours')]
        output = add_visualised_graph(
            self.load_data, start_date, end_date, models, {})
        assert_array_equal(output['data'][0]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0), datetime(2018, 1, 4, 0)])
        assert_array_equal(output['data'][0]['y'], [222, 333, 444])
        assert_array_equal(output['data'][1]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0), datetime(2018, 1, 4, 0)])
        assert_array_equal(output['data'][1]['y'], [111, 222, 333])
        self.assertEqual(len(output['data']), 2)

    def test_return_ranged_and_displaced_out_of_range(self):
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        models = [dict(model_name='model 1', model_type='displacement', model_color='red', displacement_value=96,
                           displacement_unit='Half Hours')]
        output = add_visualised_graph(
            self.load_data, start_date, end_date, models, {})
        assert_array_equal(output['data'][0]['x'], [datetime(
            2018, 1, 2, 0), datetime(2018, 1, 3, 0)])
        assert_array_equal(output['data'][0]['y'], [222, 333])
        self.assertEqual(len(output['data']), 1)


    def test_return_none_both_date_none(self):
        start_date = None
        end_date = None
        models = [dict(model_name='model 1', model_color='red', displacement_value=96,
                           displacement_unit='Half Hours')]
        output = add_visualised_graph(self.load_data, start_date, end_date, models, {})
        self.assertEqual(output, None)

    def test_return_none_end_date_none(self):
        start_date = datetime(2019, 1, 1)
        end_date = None
        models = [dict(model_name='model 1', model_color='red', displacement_value=96,
                           displacement_unit='Half Hours')]        
        output = add_visualised_graph(self.load_data, start_date, end_date, models, {})
        self.assertEqual(output, None)
        
    def test_return_none_start_date_none(self):
        start_date = None
        end_date = datetime(2019, 1, 1)
        models = [dict(model_name='model 1', model_color='red', displacement_value=96,
                           displacement_unit='Half Hours')]      
        output = add_visualised_graph(self.load_data, start_date, end_date, models, {})
        self.assertEqual(output, None)