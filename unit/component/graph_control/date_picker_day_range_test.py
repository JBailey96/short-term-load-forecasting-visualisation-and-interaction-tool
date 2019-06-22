import unittest
from datetime import datetime
from component.graph_control.date_picker_day_range import change_date

class ChangeDateRangeTest(unittest.TestCase):
    def test_return_date_decrement(self):
        increment = '0'
        decrement = '1'
        date = '2019-01-01'
        other_date = '2019-01-03'
        decrement_unit = 'Days'
        decremented_date = change_date(
            increment, decrement, date, other_date, decrement_unit)
        self.assertEqual(decremented_date, datetime(2018, 12, 31))

    def test_return_date_increment(self):
        increment = '1'
        decrement = '0'
        date = '2019-01-01'
        other_date = '2019-01-02'
        increment_unit = 'Weeks'
        incremented_date = change_date(
            increment, decrement, date, other_date, increment_unit)
        self.assertEqual(incremented_date, datetime(2019, 1, 8))

    def test_return_date_other_date_none(self):
        increment = '1'
        decrement = '0'
        date = '2019-01-01'
        other_date = None
        increment_unit = 'Weeks'
        new_date = change_date(
            increment, decrement, date, other_date, increment_unit)
        self.assertEqual(new_date, '2019-01-01')

    def test_return_none_date_none_after_initial_load(self):
        increment = '1'
        decrement = '0'
        date = None
        other_date = '2019-01-01'
        increment_unit = 'Weeks'
        new_date = change_date(
            increment, decrement, date, other_date, increment_unit)
        self.assertEqual(new_date, None)