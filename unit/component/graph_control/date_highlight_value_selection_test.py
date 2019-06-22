import unittest
import pandas as pd
from mock import patch
from component.graph_control.date_highlight_value_selection import get_options
from data.data import load_data
from datetime import datetime

class GetOptionsTest(unittest.TestCase):
    years = [2016, 2017, 2018]
    @patch('component.graph_control.date_highlight_value_selection.years', years)
    def test_return_year_options(self):
        expected_options = [{'label': 2016, 'value': 2016}, {'label': 2017, 'value':2017},
        {'label':2018, 'value':2018}]
        actual_options = get_options('Year')
        self.assertEqual(actual_options, expected_options)

    def test_return_month_options(self):
        expected_options = [{'label': 'January', 'value': 1}, {'label': 'February', 'value':2},
        {'label': 'March', 'value':3}, {'label': 'April', 'value':4}, {'label': 'May', 'value': 5}, 
        {'label': 'June', 'value': 6}, {'label': 'July', 'value': 7}, {'label': 'August', 'value': 8},
        {'label': 'September', 'value': 9}, {'label': 'October', 'value': 10}, {'label': 'November', 'value': 11},
        {'label': 'December', 'value': 12}]
        actual_options = get_options('Month')
        self.assertEqual(actual_options, expected_options)

    def test_return_season_options(self):
        expected_options = [{'label': 'Spring', 'value': 1}, {'label': 'Summer', 'value': 2}, {'label': 'Autumn', 'value': 3},
        {'label': 'Winter', 'value': 4}]
        actual_options = get_options('Season')
        self.assertEqual(actual_options, expected_options)

    def test_return_day_options(self):
        expected_options = [{'label': 'Monday', 'value': 0}, {'label': 'Tuesday', 'value': 1}, {'label': 'Wednesday', 'value': 2},
        {'label': 'Thursday', 'value': 3}, {'label': 'Friday', 'value': 4}, {'label': 'Saturday', 'value': 5}, 
        {'label': 'Sunday', 'value': 6}, {'label': 'Weekend', 'value': 'Weekend'}, {'label': 'Workday', 'value': 'Workday'}]
        actual_options = get_options('Day')
        self.assertEqual(actual_options, expected_options)

    holidays = ['Holiday 1', 'Holiday 2']
    @patch('component.graph_control.date_highlight_value_selection.holidays', holidays)
    def test_return_holiday_options(self):
        expected_options = [{'label': 'Holiday 1', 'value': 'Holiday 1'}, {'label': 'Holiday 2', 'value': 'Holiday 2'}, {'label': 'All Holidays', 'value': 'All'}]
        actual_options = get_options('Holiday')
        self.assertEqual(actual_options, expected_options)

    def test_return_no_options(self):
        expected_options = []
        actual_options = get_options('None')
        self.assertEqual(actual_options, expected_options)