import plotly.express as px
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
# import matplotlib.image as plt
# import numpy as np

def total_per_location(df):
    # df = df.drop(columns=['dir','veh_class'])
    df = df.drop(columns=['veh_class'])
    df = df.groupby(['location','dt','lat','lon'],as_index=False).agg({'value': 'sum'})
    return df

def select_latest_times(df):
    latest_time = df['dt'].max()
    df = df.loc[df['dt'] == latest_time]
    return df

def filter_logic(df, filter_1, filter_2):
    if filter_2 == None: 
        pass # full df if 2nd filter not triggered
    elif not filter_2: 
        pass # full df if 2nd filter is now []
    elif df[df[filter_1].isin(filter_2)].empty: 
        pass # full df if 1st filter changed - 2nd filter not in 1st
    else:
        df = df[df[filter_1].isin(filter_2)] # else filter 1st by 2nd
    return df

def assign_colors(df, val):
    color = dict(zip(df[val].unique(), px.colors.qualitative.Light24_r))
    df['color'] = df[val].map(color)
    return df

def datetime_to_nearest_hour(df):
    df['dt'] = df['dt'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d %H:%M:%S')
    df['dt'] = df['dt'].dt.floor('H') #.floor for previous hour, .round for nearest hour
    return df

def aggregate(df):
    # df = datetime_to_nearest_hour(df)
    df = df.groupby(
        ['location','dt','veh_class','lat','lon'], 
        sort=False, 
        as_index=False)['value'].sum()
    return df

def get_start_end_date(day_period=3):
    start_date = datetime.now()-relativedelta(days=day_period)
    end_date   = datetime.now()
    start_date = datetime.strftime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date   = datetime.strftime(end_date, '%Y-%m-%d %H:%M:%S')
    return start_date, end_date

# def resize_img(filepath):
#     img = plt.imread(filepath)
#     w, h = img.shape[:2]
#     x = int(w*1/2)
#     y = int(h*1/2)
#     xs = x/(w-1)
#     ys = y/(h-1)
#     image = np.zeros([x,y,4])
#     for i in range(x-1):
#         for j in range(y-1):
#             image[i+1,j+1] = img[1+int(i/xs), 1+int(j/ys)]
#     img.imsave(filepath, image)
#     print('resized image: '+filepath)
    