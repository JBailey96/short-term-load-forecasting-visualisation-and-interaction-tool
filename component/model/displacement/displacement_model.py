from datetime import datetime, timedelta
from data.util.data_characteristics import min_date, max_date
import pandas as pd

#calculate the date to build the displacement model from/to
def calculate_date(date, displacement_value, displacement_unit):
    minute_map = {
        'Half Hours': 30,
        'Hours': 60,
        'Days': 1440,
        'Weeks': 10080,
        'Months': 40320,
        'Years': 524160
    }
    date = datetime.strptime(date, "%Y-%m-%d")
    displacement_minutes = minute_map.get(displacement_unit) #get minute value of displacement unit chosen
    return date - timedelta(minutes=displacement_minutes*displacement_value) #displace date

#returns the displacement model forecast data
def predict(load_data, start_date, end_date, model):
    displacement_value = model['displacement_value']
    displacement_unit = model['displacement_unit']
    start_date = calculate_date(
        start_date, displacement_value, displacement_unit)
    end_date = calculate_date(end_date, displacement_value, displacement_unit)
    
    time_displaced_load_data = load_data[(load_data.Date >= start_date) & (load_data.Date <= end_date)]
    return time_displaced_load_data

    