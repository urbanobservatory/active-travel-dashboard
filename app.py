import os
import dash
from dash import ctx
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import htmlLayout
import figures
import utils
import get_video_counts_and_locations as getData
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

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
    Output('Signal-1', 'data'), 
    # Input('interval-component', 'n_intervals'), 
    Input('Filter-2', 'value'))
def compute_value(filter_2_val):
    # TODO: Cache dataframe so that don't have to re-request each time,
    # Only overwrite cache when interval-component refreshes, and send new 
    # callback to update dcc.store.
    if str(os.getenv('test')) == 'True': data = pd.read_csv('test.csv')
    else: data = getData.run()
    data = utils.assign_colors(data, filter_2_val)
    return data.to_json(orient='split', date_format='iso')

@app.callback(
    Output('Signal-2', 'data'),
    Input('Signal-1', 'data'), 
    Input('Filter-2', 'value'),
    Input('Filter-3', 'value'))
def chained_filter(data, filter_2_val, filter_3_val):
    data = pd.read_json(data, orient='split')
    data = utils.filter_logic(data, filter_2_val, filter_3_val)
    return data.to_json(orient='split', date_format='iso')

@app.callback(
    Output('Filter-3', 'options'),
    Input('Signal-1', 'data'), 
    Input('Filter-2', 'value'))
def update_filter_3(data, filter_2_val):
    df = pd.read_json(data, orient='split')
    options = df[filter_2_val].unique().tolist()
    return options

@app.callback(
    Output('Indicator-1', 'figure'),
    Input('Signal-2', 'data'))
def update_indicator_1(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Records')

@app.callback(
    Output('Indicator-2', 'figure'),
    Input('Signal-2', 'data'))
def update_indicator_2(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Locations')

@app.callback(
    Output('Indicator-3', 'figure'),
    Input('Signal-2', 'data'))
def update_indicator_3(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Vehicle Classes')

@app.callback(
    Output('Indicator-4', 'figure'),
    Input('Signal-2', 'data'))
def update_indicator_4(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Directions')

@app.callback(
    Output('Graph-1', 'figure'),
    Input('Signal-2', 'data'), 
    Input('Filter-2', 'value'))
def update_graph_1(data, filter_2_val):
    df = pd.read_json(data, orient='split')
    return figures.pxBar(df, filter_2_val)

@app.callback(
    Output('Graph-2', 'figure'),
    Input('Signal-2', 'data'), 
    Input('Filter-2', 'value'))
def update_graph_2(data, filter_2_val):
    df = pd.read_json(data, orient='split')
    df = utils.select_latest_times(df)
    fig = figures.pxPie(df, filter_2_val)
    return fig

@app.callback(
    Output('Graph-3', 'figure'),
    Input('Signal-2', 'data'),
    Input('Filter-2', 'value'))
def update_graph_3(data, filter_2_val):
    df = pd.read_json(data, orient='split')
    df = utils.total_per_location(df)
    df = utils.select_latest_times(df)
    return figures.goScatterGeo(df)

if __name__ == "__main__":
    if str(os.getenv('debug')) == 'True': d=True
    else: d=False
    app.run_server(debug=d)