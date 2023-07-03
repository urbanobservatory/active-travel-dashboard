# USE: run.py
# gets a bit of data from all available locations, then goes one by one and gets their geolocations
# api config in l 16-19

import os
import time
import warnings
# warnings.filterwarnings("ignore")
import pandas as pd
import requests
import datetime
from dash_data import utils
import median_pictures_from_s3
from dotenv import load_dotenv
load_dotenv('/env/.env')

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

url = os.getenv('url')
username = os.getenv('username')
secret = os.getenv('secret')
token = os.getenv('token')

def refresh_token(url, user, secret):
    e = url + '/refresh_token'
    d = {'device_id': user, 'secret': secret}
    response = requests.put(url=e, json=d)
    resp_j = response.json()
    token = resp_j['token']
    return token

def get_data(url, user, token, location, from_s, to_s):
    e = url + '/traffic/counts1h'
    d = {
        'user': user,
        'token': token,
        'location': location,
        'from': from_s,
        'to': to_s
    }
    response = requests.get(url=e, json=d)
    return response

# def get_locations(url, user, token, location):
#     e = url + '/traffic/sensors'
#     d = {
#         'user': user,
#         'token': token,
#         'location': location
#     }
#     response = requests.get(url=e, json=d)
#     return response

def process_data(df):
    df = df.drop('dir', axis=1)
    df = utils.aggregate(df)
    return df

def run():
    token = refresh_token(url,username,secret)  # a token is valid for 24hrs
    week = 10080
    day = 1440
    offset = 720

    for i in range(30, week, offset):
        print('fetching data: ', i)
        # get complete hours data
        past = (datetime.datetime.utcnow() - datetime.timedelta(minutes=i+offset)).strftime("%Y-%m-%d %H:%M:00")
        current = (datetime.datetime.utcnow() - datetime.timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:00")

        # get counts for 'all' locations - can be substituted with a specific location name
        data = get_data(url,username,token,'all',past, current)
        df = pd.DataFrame(data.json())
        df = df[['dir','location','dt','veh_class','value']]

        ldf = pd.read_csv('location_coordinates.csv')
        df = pd.merge(df, ldf, on=['location'])
        df['dt'] = pd.to_datetime(df['dt'])

        df = process_data(df)
        df.to_csv(f'/cache/test{i}.csv')

if __name__ == '__main__':
    while True:
        df = run()
        print('fetching images')
        median_pictures_from_s3.get_images()
        print('sleeping')
        time.sleep(300)