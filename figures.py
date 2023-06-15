import plotly.express as px
import plotly.graph_objects as go
import themes

def pxBar(df, filter_val):
    df['text']=df['location'].astype(str)+', '+df['dir'].astype(str)
    fig = px.bar(df, x='dt', y='value', color=filter_val, hover_name='text',
        color_discrete_map=dict(zip(df[filter_val], df['color'])))
    fig = themes.one(fig)
    fig.update_layout(showlegend=False, transition_duration=500)
    return fig

def pxScatterGeo(df):
    fig = px.scatter_geo(df, lat='lat', lon='lon', color='color',
            projection='natural earth', fitbounds='locations', center={
                'lat': df['lat'].median(), 
                'lon': df['lon'].median()})
    return fig

def goScatterGeo(df):
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        # name=group,
        text=df['location'].astype(str)+': '+df['value'].astype(str),
        lon=df['lon'],
        lat=df['lat'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=20, opacity=0.5, symbol='circle', color=df['value'],
            colorscale='viridis_r', cmax=df['value'].max(), showscale=True
        )
    ))
    fig.update_layout(
        title = {'text': 'Map', 'x': 0.5},
        autosize = True,
        transition_duration=500,
        # height = 1236,
        margin = {'t':30, 'b':10, 'l':10, 'r':0},
        mapbox = {
            'style': 'carto-positron', 
            'center': go.layout.mapbox.Center(
                lat=df['lat'].median(), 
                lon=df['lon'].median()), 
            'zoom': 9.7 })
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
    elif filter_val=='Vehicle Classes':
        value=df['veh_class'].nunique()
    elif filter_val=='Directions':
        value=df['dir'].nunique()
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