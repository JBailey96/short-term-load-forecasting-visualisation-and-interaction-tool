import calendar
import holidays


def add_year(load_data):
    load_data['Year'] =   load_data.apply(lambda row: row['Date'].year, axis=1)
    return load_data

def add_month(load_data):
    load_data['Month'] =   load_data.apply(lambda row: row['Date'].month, axis=1)
    return load_data

def add_season(load_data):
    load_data['Season'] = load_data.apply(lambda row: calculate_season(row['Date']), axis=1)
    return load_data

def add_day(load_data):
    load_data['Day'] = load_data.apply(lambda row: row['Date'].weekday(), axis=1)
    return load_data

def add_day_of_year(load_data):
    load_data['Dayofyear'] = load_data.apply(lambda row: row['Date'].dayofyear, axis=1)
    return load_data

def add_is_weekend(load_data):
    load_data['Is_Weekend'] = load_data.apply(lambda row: row['Date'].isoweekday() > 5, axis=1)
    return load_data

def add_holiday(load_data, country, prov=None, state=None):
    load_data['Holiday'] = load_data.apply(lambda row: calculate_holiday(row['Date'], country, prov, state), axis=1)
    return load_data

def calculate_holiday(date, country, prov, state):
    holiday_list = getattr(holidays, country)(prov=prov, state=state)
    holiday = holiday_list.get(date)

    if holiday == None:
        return 'Non-Holiday'
    return holiday

def calculate_season(date):
    spring = ['March', 'April', 'May']
    summer = ['June', 'July','August']
    autumn = ['September', 'October', 'November']

    month = calendar.month_name[date.month]
    
    if (month in spring):
        return 1
    elif (month in summer):
        return 2
    elif (month in autumn):
        return 3
    return 4