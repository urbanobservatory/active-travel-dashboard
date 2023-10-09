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
          html.H3('Select Modes of Travel:'),
          html.Br(),
          html.Div([
            dbc.Button(
              'All',
              id='all-travel-button',
              n_clicks=0,
              className='me-1',
              outline=True,
              color='primary',
              size='lg',
            ),
            dbc.Button(
              'Active Travel',
              id='active-travel-button',
              n_clicks=0,
              className='me-1',
              outline=True,
              color='primary',
              size='lg'
            ),
            dbc.Button(
              'Vehicle Travel',
              id='vehicle-travel-button',
              n_clicks=0,
              className='me-1',
              outline=True,
              color='primary',
              size='lg'
            )
          ], className='d-grid gap-2'),
          html.Br(),
          dcc.Dropdown(
            id='Filter',
            multi=True,
            placeholder='All',
            options=[
              'person','car','cyclist','buggy','goods vehicle','motorcycle',
              'bus','scooter','van','truck'
            ],
            value=['person','cyclist','scooter']
          ),
        ], className='selection box')
      ], xs=12, sm=12, md=12, lg=3, xl=3),
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
      ], xs=12, sm=12, md=12, lg=9, xl=9)
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