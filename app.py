import os
import dash
from dash import ctx, no_update
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
    Output('all-data', 'data'), 
    Input('interval-component', 'n_intervals')
)
def get_data(n):
    if str(os.getenv('test')) == 'True': data = pd.read_csv('test.csv')
    else: data = getData.run()
    return data.to_json(orient='split', date_format='iso')

@app.callback(
    Output('filtered-data', 'data'),
    Input('all-data', 'data'), 
    Input('Filter-2', 'value'),
    Input('Filter-3', 'value'))
def chained_filter(data, f2, f3):
    data = pd.read_json(data, orient='split')
    data = utils.filter_logic(data, f2, f3)
    data = utils.assign_colors(data, f2)
    return data.to_json(orient='split', date_format='iso')

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
    Output('Indicator-4', 'figure'),
    Input('filtered-data', 'data'))
def update_indicator_4(data):
    df = pd.read_json(data, orient='split')
    return figures.goIndicator(df, 'Directions')

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
    Input('Filter-2', 'value'))
def update_graph_2(data, f2):
    df = pd.read_json(data, orient='split')
    df = utils.select_latest_times(df)
    fig = figures.pxPie(df, f2)
    return fig

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
    Input('Filter-3', 'value')
)
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
    app.run_server(debug=d)