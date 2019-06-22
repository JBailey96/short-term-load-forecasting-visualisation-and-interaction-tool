import unittest
import pandas as pd
from pandas.testing import assert_frame_equal 
from datetime import datetime
from preprocessing.process_csv_util import add_season, add_day, add_is_weekend, add_month, add_year, add_holiday, add_day_of_year

class AddYear(unittest.TestCase):

    def test_return_dataframe_year_column(self):
        test_d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2016, 1, 2, 0), datetime(2015, 1, 3, 0),
                      datetime(2014, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2016, 1, 2, 0), datetime(2015, 1, 3, 0),
                      datetime(2014, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Year': [2018, 2018, 2016, 2015, 2014]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_year(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_dataframe_year_column_already_exists(self):
        test_d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2016, 1, 2, 0), datetime(2015, 1, 3, 0),
                      datetime(2014, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Year': [2018, 2018, 2016, 2015, 2014]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2016, 1, 2, 0), datetime(2015, 1, 3, 0),
                      datetime(2014, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Year': [2018, 2018, 2016, 2015, 2014]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_year(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)

class AddMonth(unittest.TestCase):
    def test_return_dataframe_month_column(self):
        test_d = {'Date': [datetime(2018, 3, 1, 0), datetime(2018, 4, 1, 1), datetime(2016, 5, 2, 0), datetime(2015, 7, 3, 0),
                      datetime(2014, 8, 3, 0)], 'Load': [111, 222, 333, 444, 555]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 3, 1, 0), datetime(2018, 4, 1, 1), datetime(2016, 5, 2, 0), datetime(2015, 7, 3, 0),
                      datetime(2014, 8, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Month': [3, 4, 5, 7, 8]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_month(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)

class AddSeason(unittest.TestCase):
    def test_return_spring_start(self):
        test_d = {'Date': [datetime(2018, 3, 1, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 3, 1, 0)], 'Load': [111], 'Season': [1]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_season(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)
    
    def test_return_spring_end(self):
        test_d = {'Date': [datetime(2018, 5, 31, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 5, 31, 0)], 'Load': [111], 'Season': [1]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_season(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)  

    def test_return_summer_start(self):
        test_d = {'Date': [datetime(2018, 6, 1, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 6, 1, 0)], 'Load': [111], 'Season': [2]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_season(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)
    
    def test_return_summer_end(self):
        test_d = {'Date': [datetime(2018, 8, 31, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 8, 31, 0)], 'Load': [111], 'Season': [2]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_season(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_autumn_start(self):
        test_d = {'Date': [datetime(2018, 9, 1, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 9, 1, 0)], 'Load': [111], 'Season': [3]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_season(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_autumn_end(self):
        test_d = {'Date': [datetime(2018, 11, 30, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 11, 30, 0)], 'Load': [111], 'Season': [3]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_season(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_winter_start(self):
        test_d = {'Date': [datetime(2018, 12, 1, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 12, 1, 0)], 'Load': [111], 'Season': [4]}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_season(load_data)
        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_winter_end(self):
        test_d = {'Date': [datetime(2018, 2, 28, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 2, 28, 0)], 'Load': [111], 'Season': [4]}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_season(load_data)
        assert_frame_equal(expected_load_data, actual_load_data)

class AddDay(unittest.TestCase):
    def test_return_day(self):
        test_d = {'Date': [datetime(2019, 1, 15, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2019, 1, 15, 0)], 'Load': [111], 'Day': [1]}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_day(load_data)
        assert_frame_equal(expected_load_data, actual_load_data)

class AddIsWeekend(unittest.TestCase):
    def test_return_is_weekend_true(self):
        test_d = {'Date': [datetime(2019, 1, 19, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2019, 1, 19, 0)], 'Load': [111], 'Is_Weekend': [True]}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_is_weekend(load_data)
        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_is_weekend_false(self):
        test_d = {'Date': [datetime(2019, 1, 21, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2019, 1, 21, 0)], 'Load': [111], 'Is_Weekend': [False]}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_is_weekend(load_data)
        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_is_weekend_false_monday(self):
        test_d = {'Date': [datetime(2018, 1, 8, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 1, 8, 0)], 'Load': [111], 'Is_Weekend': [False]}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_is_weekend(load_data)
        assert_frame_equal(expected_load_data, actual_load_data)

class AddHoliday(unittest.TestCase):
    def test_return_holiday_christmas(self):
        test_d = {'Date': [datetime(2019, 12, 25, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2019, 12, 25, 0)], 'Load': [111], 'Holiday': ['Christmas Day']}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_holiday(load_data, country='NorthernIreland')
        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_not_holiday(self):
        test_d = {'Date': [datetime(2019, 12, 29, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2019, 12, 29, 0)], 'Load': [111], 'Holiday': ['Non-Holiday']}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_holiday(load_data, country='NorthernIreland')
        assert_frame_equal(expected_load_data, actual_load_data)

    def test_return_state_province_holiday(self):
        test_d = {'Date': [datetime(2019, 12, 25, 0)], 'Load': [111]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2019, 12, 25, 0)], 'Load': [111], 'Holiday': ['Christmas Day']}
        expected_load_data = pd.DataFrame(data=expected_d)

        actual_load_data = add_holiday(load_data, country='UnitedStates', prov='AB', state='CA')
        assert_frame_equal(expected_load_data, actual_load_data)


class AddDayOfYear(unittest.TestCase):
     def test_return_dataframe_doy_column(self):
        test_d = {'Date': [datetime(2018, 1, 1), datetime(2018, 1, 2), datetime(2018, 1, 3), datetime(2018, 1, 4),
                      datetime(2018, 12, 31)], 'Load': [111, 222, 333, 444, 555]}
        load_data = pd.DataFrame(data=test_d)

        expected_d = {'Date': [datetime(2018, 1, 1), datetime(2018, 1, 2), datetime(2018, 1, 3), datetime(2018, 1, 4),
                      datetime(2018, 12, 31)], 'Load': [111, 222, 333, 444, 555], 'Dayofyear': [1, 2, 3, 4, 365]}
        expected_load_data = pd.DataFrame(data=expected_d)
        
        actual_load_data = add_day_of_year(load_data)

        assert_frame_equal(expected_load_data, actual_load_data)