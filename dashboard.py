'''----------------------------------------------------------------------------
Name:        Ontario Coronavirus Dashboard (dashboard.py)
Purpose:     To display coronavirus data in a visually pleasing and effective
             manner.

Author:      Nicholas Chong
Created:     2020-07-03 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from site_data.get_data import *
import time
from datetime import datetime, timedelta
from dash.dependencies import ClientsideFunction, Input, Output

# Create Dash app instance
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',           # Dash CSS
    'https://unpkg.com/boxicons@2.0.5/css/boxicons.min.css' # Icon pack
]
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {
            'property': 'twitter:card',
            'content': 'summary_large_image',
        },
        {
            'property': 'twitter:title',
            'content': 'Ontario Coronavirus Summary',
        },
        {
            'property': 'twitter:description',
            'content': 'Interactive Ontario coronavirus dashboard.',
        },
        {
            'property': 'twitter:image',
            'content': 'http://mighty-gorge-03520.herokuapp.com/assets/dashboard_img_twitter.jpg',
        },
        {
            'property': 'og:image',
            'prefix': 'og: http://ogp.me/ns#',
            'content': '/assets/dashboard_img.png',
        },
        {
            'property': 'og:url',
            'prefix': 'og: http://ogp.me/ns#',
            'content': 'http://tinyurl.com/coronavirus-graphs',
        },
    ],
)
server = app.server
app.title = 'Ontario Coronavirus Summary'

# Create Figures
fig1 = px.line(data_frame=df, x='Date', y=['New Cases', '7 Day Average'], title='Daily New Cases')
fig2 = px.line(data_frame=df, x='Date', y='Total Cases', title='Total Cases')
fig3 = px.line(data_frame=df, x='Date', y='New Deaths', title='Daily New Deaths')
fig4 = px.line(data_frame=df, x='Date', y='Tests Completed', title='Daily Tests Completed')
fig5 = px.line(data_frame=df, x='Date', y='Percent Positive', title='Daily Percent Positive')

figs_list = [fig1, fig2, fig3, fig4, fig5]
[i.update_layout(yaxis=dict(fixedrange=True)) for i in figs_list]

# Create layout (html generation using dash_html_components)
app.layout = html.Div(
    [
        html.Div (
            [
                html.H1(
                    'Ontario Coronavirus Summary',
                    style={
                        'textAlign' : 'center',
                    },
                ),

                html.H5(
                    'Wear a mask! Flatten the curve!',
                    style={
                        'textAlign' : 'center',
                        'padding-bottom' : '20px',
                    }
                )
            ]
        ), 

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    df.iloc[-1]['New Cases']
                                ), 
                                
                                html.P(
                                    f'New Cases ({df.iloc[-1]["Date"]})'
                                ),

                                html.P(
                                    dod_new_cases[0],
                                    style={
                                        'color' : dod_new_cases[1]
                                    }
                                )
                            ],

                            className='mini_container',
                        ),

                        html.Div(
                            [
                                html.H6(
                                    df.iloc[-1]['New Deaths']
                                ), 
                                
                                html.P(
                                    f'New Deaths ({df.iloc[-1]["Date"]})'
                                ),

                                html.P(
                                    dod_new_deaths[0],
                                    style={
                                        'color' : dod_new_deaths[1]
                                    }
                                )
                            ],

                            className='mini_container',
                        ),

                        html.Div(
                            [
                                html.H6(
                                    df.iloc[-1]['Total Cases']
                                ), 
                                
                                html.P(
                                    'Total Cases'
                                )
                            ],

                            className='mini_container',
                        ),

                        html.Div(
                            [
                                html.H6(
                                    df.iloc[-1]['Total Deaths']
                                ), 

                                html.P(
                                    'Total Deaths'
                                )
                            ],

                            className='mini_container',
                        ),
                    ],

                    id='info-container',
                    className='container-display',
                )
            ]
        ),

        dcc.Store(
            id='clientside_datastore',
            data={}
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.DatePickerRange(
                            id='datepicker',
                            display_format='YYYY-MM-DD',
                            min_date_allowed=df['Date'].min(),
                            max_date_allowed=df['Date'].max()+timedelta(days=1),
                            start_date=df['Date'].min(),
                            end_date=df['Date'].max(),
                            updatemode='bothdates',
                            initial_visible_month=df['Date'].max()
                        ),

                        html.H6(
                            'foo',
                            id='datepicker_output'
                        ),

                        html.Div(
                            [
                                html.Button(
                                    'Reset',
                                    id='reset_graphs_button',
                                    n_clicks=0
                                )
                            ],
                            style={
                                'margin-left': 'auto',
                            }
                        )
                    ],
                    className='mini_container',
                    style={
                        'display': 'flex',
                        'align-items': 'center',
                    }
                ),
            ],
            id='datepicker_container',
            className='container-display',
            style={
                'display': 'flex',
            }
        ),

        html.Div(
            [
                dcc.Graph(figure=fig1, id='graph1', animate=True),
            ],

            className='pretty_container',
        ),

        html.Div(
            [
                dcc.Graph(figure=fig2, id='graph2'),
            ],

            className='pretty_container'
        ),
        
        html.Div(
            [
                dcc.Graph(figure=fig3, id='graph3'),
            ],

            className='pretty_container'
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(figure=fig4, id='graph4'),
                    ],

                    className='pretty_container',
                    style={
                        'width' : '50%',
                    }
                ),

                html.Div(
                    [
                        dcc.Graph(figure=fig5, id='graph5'),
                    ],

                    className='pretty_container',
                    style={
                        'width' : '50%',
                    }
                ),
            ],

            style={
                'display' : 'flex',
            }
        ),

        html.Div(
            [
                html.P(
                    '''
                    Not affiliated with the Ontario Government. Data obtained
                    from the Ontario Government data catalogue.
                    ''',
                    style={
                        'font-size' : 'x-small',
                        'textAlign' : 'center',
                    }
                ),

                html.Div(
                    [
                        html.A(
                            html.I(
                                className='bx bxl-github bx-tada',
                                style={
                                    'font-size': 'x-large'
                                }
                            ),
                            href='https://github.com/Nicholas-Chong/COVID-19-Twitter-Bot-and-Dashboard',
                            target='_blank',
                        ),

                        html.A(
                            html.I(
                                className='bx bxl-twitter bx-tada',
                                style={
                                    'font-size': 'x-large',
                                    'padding-left': '10px'
                                }
                            ),
                            href='https://twitter.com/OntarioCovid19',
                            target='_blank',
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'text-align': 'center',
                        'justify-content': 'center',
                    }
                ),
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
            }
        ),
    ]
)


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_daterange',
    ),
    [
        Output('datepicker_output', 'children'), 
        Output('clientside_datastore', 'data'),
    ],
    [
        Input('datepicker', 'start_date'),
        Input('datepicker', 'end_date'),
        Input('reset_graphs_button', 'n_clicks'),
    ]
)

@app.callback(
    [
        Output('graph1', 'figure'), 
        Output('graph2', 'figure'), 
        Output('graph3', 'figure'), 
        Output('graph4', 'figure'), 
        Output('graph5', 'figure'), 
        Output('datepicker', 'start_date'),
        Output('datepicker', 'end_date'),
    ],
    [Input('clientside_datastore', 'data')]
)
def update_graphs(xrange):
    '''
    Updates graphs for a particular xrange by returning new figures
    '''

    # Extract start and end dates (as strings) from xrange
    start = xrange['start']
    end = xrange['end']

    # Copy figs that were created at start 
    newfig1 = fig1
    newfig2 = fig2
    newfig3 = fig3
    newfig4 = fig4
    newfig5 = fig5
    newfigs = [newfig1, newfig2, newfig3, newfig4, newfig5]

    # Update newfigs layouts with new xrange (start, end)
    [i.update_layout(transition_duration=500, xaxis_range=(start, end)) 
    for i in newfigs]

    return [newfig1, newfig2, newfig3, newfig4, newfig5, start, end]


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
