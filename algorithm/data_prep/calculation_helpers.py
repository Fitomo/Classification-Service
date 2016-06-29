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

def date_difference(date, days, before_or_after):
    if before_or_after == 'before':
        time = dt.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
        date_before = (time - dt.timedelta(days=days)).strftime('%Y%m%d')
        return date_before
    else:
        time = dt.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
        date_after = (time + dt.timedelta(days=days)).strftime('%Y%m%d')
        return date_after

def find_days_before_slope(df, user_id, date, category, days):
    curr_date = pd.to_datetime(date, format='%Y-%m-%d')
    df = df[df['user_id']==user_id]
    if curr_date in df.index:
        days_before_amt = find_data(df, user_id, date, category, days)
        if days_before_amt > 0:
            curr_stat = df.ix[curr_date, category]
            slope = (curr_stat - days_before_amt) / days
        else:
            slope = None
        return slope
    else:
        return None

def find_data(df, user_id, date, category, days):
    if category == 'curr_health_score':
        target_date = pd.to_datetime(date_difference(date, days, 'after'))
    else:
        target_date = pd.to_datetime(date_difference(date, days, 'before'))
    df = df[df['user_id']==user_id]
    if target_date in df.index:
        result = df.ix[target_date, category]
        return result
    else:
        return None
