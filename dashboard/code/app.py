import os
import dash
from dash import ctx, no_update, Patch
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import htmlLayout
import figures
from dash_data import utils
import pandas as pd
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
load_dotenv('/env/.env')

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{
        'name': 'viewport', 
        'content': 'width=device-width, initial-scale=1.0'
    }]
)
server = app.server
app.layout = htmlLayout.layout()

@app.callback(
    Output('all-data', 'data'), 
    Input('interval-component', 'n_intervals'))
def get_data(n):
    dfs = []
    for file in os.listdir('/cache/'):
        if '.csv' in file:
            dfs.append(pd.read_csv('/cache/'+file))
    data = pd.concat(dfs)
    data.to_csv('/code/data.csv',index=False)
    return '/code/data.csv'

@app.callback(
    Output('Filter', 'value'),
    Input('active-travel-button', 'n_clicks'),
    Input('vehicle-travel-button', 'n_clicks'),
    Input('all-travel-button', 'n_clicks'),
    prevent_initial_call=True,
)
def filter_values(active_n_clicks, vehcile_n_clicks, all_n_clicks):
    if 'active-travel-button' == ctx.triggered_id:
        value = ['person', 'cyclist', 'scooter']
    elif 'vehicle-travel-button' == ctx.triggered_id:
        value = ['car','buggy','goods vehicle','motorcycle','bus','van','truck']
    elif 'all-travel-button' == ctx.triggered_id:
        value = ['person','cyclist','scooter','car','buggy','goods vehicle',
                 'motorcycle','bus','van','truck']
    return value

@app.callback(
    Output('Indicator-1', 'figure'),
    Input('all-data', 'data'),
    Input('Filter', 'value'))
def update_indicator_1(data, value):
    df = pd.read_csv(data)
    df = df[df['veh_class'].isin(value)]
    return figures.goIndicator(df, 'Records')

@app.callback(
    Output('Indicator-2', 'figure'),
    Input('all-data', 'data'),
    Input('Filter', 'value'))
def update_indicator_2(data, value):
    df = pd.read_csv(data)
    df = df[df['veh_class'].isin(value)]
    return figures.goIndicator(df, 'Locations')

@app.callback(
    Output('Indicator-3', 'figure'),
    Input('all-data', 'data'),
    Input('Filter', 'value'))
def update_indicator_3(data, value):
    df = pd.read_csv(data)
    df = df[df['veh_class'].isin(value)]
    return figures.goIndicator(df, 'Travel Modes')

@app.callback(
    Output('Graph-1', 'figure'),
    Input('all-data', 'data'),
    Input('Filter', 'value'))
def update_graph_1(data, value):
    df = pd.read_csv(data)
    df = df[df['veh_class'].isin(value)]
    # df.sort_values('location')
    return figures.pxBar(df)

# TODO: Updates graph 1 location colors based on map hover. Match df index
#  locations with patched figure locations
# @app.callback(
#     Output('Graph-1','figure', True),
#     Input('Graph-3','hoverData'),
#     Input('all-data','data'),
#     Input('Filter', 'value'),
#     prevent_initial_call=True)
# def update_graph_1_color(hoverData, data, value):
#     id = hoverData['points'][0]['text'].split(':')[0]
#     df = pd.read_csv(data)
#     df = df[df['veh_class'].isin(value)]
#     # df.sort_values('location')
#     locations = list(df.loc[df['location'] == id].index) # gets index positions which need to be changed in patched figure
#     patched_figure = Patch()
#     updated_markers = [
#         "white" if i in locations else "blue" for i in range(len(df))
#     ]
#     patched_figure['data'][1]['marker']['color'] = updated_markers
#     return patched_figure

@app.callback(
    Output('Graph-2', 'figure'),
    Input('all-data', 'data'),
    Input('Graph-1', 'hoverData'),
    Input('Graph-3', 'hoverData'),
    Input('Filter', 'value'))
def update_graph_2(data, g1, g3, value):
    df = pd.read_csv(data)
    df = df[df['veh_class'].isin(value)]
    if 'Filter' == ctx.triggered_id:
        raise PreventUpdate
    elif 'all-data' == ctx.triggered_id:
        random_df = df.sample().reset_index()
        random_id = random_df['location'].iloc[0]
        df = df.loc[df['location'] == random_id]
    elif 'Graph-1' == ctx.triggered_id:
        id = g1['points'][0]['hovertext'].split(':')[0]
        df = df.loc[df['location'].isin([id])]
    elif 'Graph-3' == ctx.triggered_id:
        id = g3['points'][0]['text'].split(':')[0]
        df = df.loc[df['location'].isin([id])]
    df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d %H:%M:%S')
    df.sort_values(by='dt', inplace=True)
    start_date, end_date = utils.get_start_end_date(day_period=2)
    mask = (df['dt'] > start_date) & (df['dt'] <= end_date)
    df = df.loc[mask]
    return figures.goScatter(df)

@app.callback(
    Output('Graph-3', 'figure'),
    Input('all-data', 'data'),
    Input('Filter', 'value'))
def update_graph_3(data, value):
    df = pd.read_csv(data)
    df = df[df['veh_class'].isin(value)]
    df = utils.total_per_location(df)
    df = utils.select_latest_times(df)
    return figures.goScatterGeo(df)

# https://community.plotly.com/t/displaying-image-on-point-hover-in-plotly/9223/15
@app.callback(
    Output('Graph-3-tooltip', 'show'),
    Output('Graph-3-tooltip', 'bbox'),
    Output('Graph-3-tooltip', 'children'),
    Input('Graph-3', 'hoverData'),  
    Input('Filter', 'value'))
def display_hover(hoverData, value):
    if 'Filter' == ctx.triggered_id or hoverData is None:
        return False, no_update, no_update
    else:
        bbox, children = figures.image_hover(hoverData)
        return True, bbox, children

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)