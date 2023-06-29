import plotly.express as px
import pandas as pd

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