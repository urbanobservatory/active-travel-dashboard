from dash import dcc, html
import dash_bootstrap_components as dbc

def layout():
  return dbc.Container([
    dbc.Row([
      dbc.Col([html.H1(
        'Tyne and Wear Active Travel',
        className='text-center mb-4'
      )], width=12)
    ]),

    dbc.Row([
      dbc.Col([
        html.Div([
          # html.H3('Select day:'),
          # dcc.RangeSlider(
          #   id='Filter-1',
          #   min=-7, 
          #   max=0, 
          #   step=1,
          #   count=1, 
          #   value=[-7, 0]
          # ),
          # html.Br(),
          html.H3('Display by:'),
          dcc.RadioItems(
            id='Filter-2',
            options=[
                {'label': 'Vehicle Class', 'value': 'veh_class'},
                {'label': 'Location', 'value': 'location'},
            ],
            value='veh_class'
          ),
          html.Br(),
          html.H3('Filter by:'),
          dcc.Dropdown(
            id='Filter-3',
            multi=True,
            placeholder='All'
          ),
        ], className='selection box')
      ], xs=12, sm=12, md=12, lg=4, xl=4),
      dbc.Col([
        dbc.Stack([
          dbc.Row([
            dbc.Col([
              html.Div([
                dcc.Graph(
                  id='Indicator-1', 
                  style={'width':'400px','height':'100px'}
                )
              ], className='box')
            ], xs=12, sm=12, md=4, lg=4, xl=4),
            dbc.Col([
              html.Div([
                dcc.Graph(
                  id='Indicator-2', 
                  style={'width':'400px','height':'100px'}
                )
              ], className='box')
            ], xs=12, sm=12, md=4, lg=4, xl=4),
            dbc.Col([
              html.Div([
                dcc.Graph(
                  id='Indicator-3', 
                  style={'width':'400px','height':'100px'}
                )
              ], className='box')
            ], xs=12, sm=12, md=4, lg=4, xl=4),
            # dbc.Col([
            #   html.Div([
            #     dcc.Graph(
            #       id='Indicator-4', 
            #       style={'width':'300px','height':'100px'}
            #     )
            #   ], className='box')
            # ], xs=12, sm=12, md=3, lg=3, xl=3),
          ], justify='between'),
          dbc.Row([
            dbc.Col([
              html.Div([
                dcc.Graph(
                  id='Graph-1', 
                  style={'height':'320px'}
                )
              ], className='box')
            ], xs=12, sm=12, md=12, lg=12, xl=12)
          ])
        ], gap=5)
      ], xs=12, sm=12, md=12, lg=8, xl=8)
    ], className='g-5'), # gutter size

    html.Br(),

    dbc.Row([
      dbc.Col([
        html.Div([
          dcc.Graph(
            id='Graph-3'
          ),
          dcc.Tooltip(id='Graph-3-tooltip')
        ], className='box')
      ], xs=12, sm=12, md=12, lg=7, xl=7),
      dbc.Col([
        html.Div([
          dcc.Graph(
            id='Graph-2'
          )
          # html.Img(id='image')
        ], className='box')
      ], xs=12, sm=12, md=12, lg=5, xl=5)
    ], className='g-5'),

    # Update every 5 minutes
    dcc.Interval(id='interval-component', interval=5*60000, n_intervals=0),
    dcc.Store(id='all-data'),
    dcc.Store(id='filtered-data'),

  ], fluid=True)