from datetime import datetime, timedelta
from data.data import load_data

#change the input date by a specific value and increment/decrement
def change_date(increment, decrement, date, other_date, units):
    if other_date == None: #if the other date is not set
        return date
    elif increment != decrement and date == None: #date is not set and increment or decrement has been clicked
        return None

    new_date = datetime.strptime(date, "%Y-%m-%d") #get the datetime representation of the date to perform mathmetical operations on it

    #get the mapping of minutes to increment/decrement unit selected by the user
    minute_map = {
        'Days': 1440,
        'Weeks': 10080,
        'Months': 40320,
        'Years': 524160
    }

    minutes = minute_map[units]

    if int(increment) > int(decrement): #if user clicked increment
        new_date = new_date + timedelta(minutes=minutes)
    elif int(decrement) > int(increment): #if user clicked decrement
        new_date = new_date - timedelta(minutes=minutes)

    return new_date
    