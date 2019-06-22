from data.util.data_characteristics import years, holidays

#gets the list of day type value options for a  highlight variable chosen
def get_options(highlight_variable):
    if (highlight_variable == 'Year'):
        return get_years()
    elif (highlight_variable == 'Month'):
        return get_months()
    elif (highlight_variable == 'Season'):
        return get_seasons()
    elif (highlight_variable == 'Day'):
        return get_days()
    elif (highlight_variable == 'Holiday'):
        return get_holidays()
    return []

#returns a list of years in the dataset
def get_years():
    options = []
    for year in years:
        options.append({'label': year, 'value': year})
    return options

#returns a list of month-value in year. 
def get_months():
    options = []
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    'November', 'December']
    increment = 1

    for month in months:
        options.append({'label': month, 'value': increment})
        increment += 1
    return options

#returns a list of meteorological seasons-value in the year.
def get_seasons():
    options = []
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    increment = 1
    
    for season in seasons:
        options.append({'label': season, 'value': increment})
        increment += 1
    return options 

#returns a list of days and specific types of day
def get_days():
    options = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    increment = 0

    for day in days:
        options.append({'label': day, 'value': increment})
        increment += 1
    options.append({'label': 'Weekend', 'value': 'Weekend'})
    options.append({'label':'Workday', 'value': 'Workday'})
    return options 

#returns a list of holidays in the dataset and an option for all holidays to be highlighted
def get_holidays():
    options = []
    for holiday in holidays:
        options.append({'label': holiday, 'value': holiday})
    options.append({'label': 'All Holidays', 'value': 'All'})
    return options
