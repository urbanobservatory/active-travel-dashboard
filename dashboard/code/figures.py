import os
import plotly.express as px
import plotly.graph_objects as go
import themes
from dash import html

def pxBar(df):
    df['text']=df['location'].astype(str)
    fig = px.bar(
        df, 
        x='dt', 
        y='value', 
        color='veh_class',
        hover_name='text',
        color_discrete_map=dict(zip(df['veh_class'], df['color']))
    )
    fig = themes.one(fig)
    fig.update_layout(
        title={'text': 'Active Travel Total', 'x': 0.5},
        showlegend=False,
        transition_duration=500,
        xaxis_title=None, 
        yaxis_title=None,
        margin = {'t':60, 'b':50, 'l':50, 'r':50}
    )
    return fig

def goScatter(df):
    fig = go.Figure()
    groups = df['veh_class'].unique()
    for group in groups:
        tdf = df[df['veh_class'] == group]
        print(tdf)
        fig.add_trace(go.Scatter(
            name=group, 
            x=list(tdf['dt']), 
            y=list(tdf['value']), 
            xaxis='x', 
            yaxis='y', 
            text=tdf['value'].astype(str),
            mode='lines+markers',
            marker_color=tdf['color'].iloc[0],
            line_color=tdf['color'].iloc[0],
            # line_shape='spline',
            opacity = 0.5
        ))
    fig.update_layout(
        title={'text': df['location'].iloc[0]+' (48hrs)', 'x': 0.5},
        margin = {'t':60, 'b':50, 'l':50, 'r':50},
        transition_duration=500
    )
    fig = themes.one(fig)
    return fig

def pxScatterGeo(df):
    fig = px.scatter_geo(df, lat='lat', lon='lon', color='color',
            projection='natural earth', fitbounds='locations', center={
                'lat': df['lat'].median(), 
                'lon': df['lon'].median()})
    return fig

def goScatterGeo(df):
    normalised_value = (df['value']-df['value'].min())/(df['value'].max()-df['value'].min())
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        # name=group,
        text=df['location'].astype(str)+': '+df['value'].astype(str),
        lon=df['lon'],
        lat=df['lat'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=(normalised_value*50)+10, opacity=0.5, symbol='circle', color=df['value'],
            colorscale='Bluered', cmax=df['value'].max(), showscale=True
        )
    ))
    fig.update_layout(
        autosize = True,
        transition_duration=500,
        # height = 1236,
        margin = {'t':10, 'b':10, 'l':10, 'r':0},
        mapbox = {
            'style': 'carto-positron', 
            'center': go.layout.mapbox.Center(
                lat=df['lat'].median(), 
                lon=df['lon'].median()), 
            'zoom': 9.7 })
    fig.update_traces(hoverinfo="none", hovertemplate=None)
    fig = themes.one(fig)
    return fig

def pxPie(df, filter_val):
    fig = px.pie(df, values='value', names=filter_val, color=filter_val,
        color_discrete_map=dict(zip(df[filter_val], df['color'])))
    fig.update_traces(textposition='inside', textinfo='percent+label')
    # fig.update_layout(
    #     showlegend=False,
    #     margin = {'t':0, 'b':0, 'l':10, 'r':10}
    # )
    fig = themes.one(fig)
    fig.update_layout(showlegend=False, transition_duration=500)
    return fig

def goIndicator(df, filter_val):
    if filter_val=='Records':
        value=len(df.index)
    elif filter_val=='Locations':
        value=df['location'].nunique()
    elif filter_val=='Travel Modes':
        value=df['veh_class'].nunique()
    # elif filter_val=='Directions':
    #     value=df['dir'].nunique()
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        title = {'text':filter_val, 'align':'left'},
        mode='number', 
        value=value,
        # delta={'position': "top", 'reference': 320}, 
        # domain={'row': 0, 'column': 0}, 
        align='left',
        number={'font':{'size':40}}
    ))
    fig = themes.one(fig)
    return fig

def image(path):
    fig = go.Figure()
    w = 1920
    h = 1080
    scale = 0.3
    fig.add_trace(go.Scatter(
        x=[0, w*scale],
        y=[0, h*scale],
        mode='markers',
        marker_opacity=0
    ))
    fig.update_xaxes(visible=False, range=[0, w*scale])
    fig.update_yaxes(visible=False, range=[0, h*scale], scaleanchor='x')
    fig.add_layout_image(dict(
        x=0,
        sizex=w*scale,
        y=h*scale,
        sizey=h*scale,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source=path
    ))
    fig.update_layout(
        width=w*scale,
        height=h*scale,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    return fig

def image_hover(hoverData):
    pt = hoverData['points'][0]
    location = pt['text'].split(':')[0]
    bbox = pt['bbox']

    if os.path.exists(f'/assets/{location}.jpg'):
        print('exists')
        path = f'/assets/{location}.jpg'
    else:
        path = '/assets/No_image_available.png'

    children = [
        html.Div(children=[
            html.Img(src=path, style={'width': "100%"}),
            html.H5(pt['text'], style={'text-align': 'left'}),
        ],
        style={'width': '200px', 'white-space': 'normal'})
    ]
    return bbox, children