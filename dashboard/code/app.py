import os
import dash
from dash import ctx, no_update
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import htmlLayout
import figures
from dash_data import utils
# import python_cache.code.get_video_counts_and_locations as get_video_counts_and_locations
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
    # if str(os.getenv('test')) == 'True': 
    data = pd.read_csv('/cache/test3.csv')
    # else: 
    #     data = get_video_counts_and_locations.run()
    return data.to_json(orient='split', date_format='iso')

@app.callback(
    Output('filtered-data', 'data'),
    Input('all-data', 'data'), 
    Input('Filter-2', 'value'),
    Input('Filter-3', 'value'))
def chained_filter(data, f2, f3):
    datas = pd.read_json(data, orient='split')
    datas = utils.filter_logic(datas, f2, f3)
    datas = utils.assign_colors(datas, f2)
    return datas.to_json(orient='split', date_format='iso')

@app.callback(
    Output('Filter-3', 'options'),
    Input('all-data', 'data'), 
    Input('Filter-2', 'value'))
def update_filter_3(data, f2):
    df = pd.read_json(data, orient='split')
    options = df[f2].unique().tolist()
    return options

@app.callback(
    Output('Indicator-1', 'figure'),
    Input('filtered-data', 'data'))
def update_indicator_1(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Records')

@app.callback(
    Output('Indicator-2', 'figure'),
    Input('filtered-data', 'data'))
def update_indicator_2(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Locations')

@app.callback(
    Output('Indicator-3', 'figure'),
    Input('filtered-data', 'data'))
def update_indicator_3(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Vehicle Classes')

@app.callback(
    Output('Graph-1', 'figure'),
    Input('filtered-data', 'data'), 
    Input('Filter-2', 'value'))
def update_graph_1(data, f2):
    df = pd.read_json(data, orient='split')
    return figures.pxBar(df, f2)

@app.callback(
    Output('Graph-2', 'figure'),
    Input('filtered-data', 'data'), 
    Input('Graph-1', 'hoverData'),
    Input('Graph-3', 'hoverData'))
def update_graph_2(data, g1, g3):
    df = pd.read_json(data, orient='split')
    # TODO: PREVENT UPDATES WITH FILTER TRIGGER
    if 'Filter-2' == ctx.triggered_id \
    or 'Filter-3' == ctx.triggered_id:
        raise PreventUpdate
    elif 'filtered-data' == ctx.triggered_id:
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
    df.sort_values(by='dt', inplace = True)
    mask = (df['dt'] > '2023-06-27 11:00:00') & (df['dt'] <= '2023-06-29 11:00:00') #TODO: Remove hard coding
    df = df.loc[mask]
    return figures.goScatter(df)

@app.callback(
    Output('Graph-3', 'figure'),
    Input('filtered-data', 'data'),
    Input('Filter-2', 'value'))
def update_graph_3(data, f2):
    df = pd.read_json(data, orient='split')
    df = utils.total_per_location(df)
    df = utils.select_latest_times(df)
    return figures.goScatterGeo(df)

# https://community.plotly.com/t/displaying-image-on-point-hover-in-plotly/9223/15
@app.callback(
    Output('Graph-3-tooltip', 'show'),
    Output('Graph-3-tooltip', 'bbox'),
    Output('Graph-3-tooltip', 'children'),
    Input('Graph-3', 'hoverData'),  
    Input('Filter-2', 'value'),
    Input('Filter-3', 'value'))
def display_hover(hoverData, f2, f3):
    if 'Filter-2' == ctx.triggered_id \
    or 'Filter-3' == ctx.triggered_id \
    or hoverData is None:
        return False, no_update, no_update
    else:
        bbox, children = figures.image_hover(hoverData)
        return True, bbox, children
    
if __name__ == "__main__":
    if str(os.getenv('debug')) == 'True': d=True
    else: d=False
    app.run_server(debug=d, host='0.0.0.0', port=80)