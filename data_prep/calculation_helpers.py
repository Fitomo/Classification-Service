import datetime as dt
import pandas as pd
import numpy as np

def find_mean(all_data, index):
    data = [float(row[index]) for row in all_data]
    avg = sum(data) / len(data)
    return avg

def find_percentile(all_data, index, percentile):
    data = [float(row[index]) for row in all_data]
    return np.percentile(data, percentile)

def days_before(date, days):
    time = dt.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
    date_before = (time - dt.timedelta(days=days)).strftime('%Y%m%d')
    return date_before

def find_days_before_slope(df, user_id, date, category, start, end):
    curr_date = pd.to_datetime(date, format='%Y-%m-%d')
    if curr_date in df.index:
        days_before_avg = find_days_before_data(df, user_id, date, category, start, end)
        if days_before_avg > 0:
            curr_stat = df.ix[curr_date][category]
            slope = (curr_stat - days_before_avg) / ((end + start) / 2)
        else:
            slope = 0
        return slope
    else:
        return

def find_days_before_data(df, user_id, date, category, start, end):
    min_day = pd.to_datetime(days_before(date, start), format='%Y-%m-%d')
    max_day = pd.to_datetime(days_before(date, end), format='%Y-%m-%d')
    result = df.ix[max_day:min_day]
    if len(result.index) > 0:
        mean = sum(result[category]) / len(result.index)
    else:
        mean = 0
    return mean
