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
import plotly.graph_objects as go
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
            'content': 'http://www.ontariocovid-19.com/assets/dashboard_img_twitter.jpg',
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
        {
            'name': 'viewport',
            'content': '''
                width=device-width, 
                initial-scale=0.48, 
                maximum-scale=0.48, 
                minimum-scale=0.48 ''',
        },
    ],
)
server = app.server
app.title = 'Ontario Coronavirus Summary'

# Create Figures
fig1 = (
    px.line(
        data_frame=df, x='Date', y=['New Cases', '7 Day Average'], 
        title='Daily New Cases',
    )
    .update_layout(showlegend=False, margin={'r': 30})
)
fig2 = px.line(
    data_frame=df, x='Date', y='Total Cases', title='Total Cases'
)
fig3 = px.line(
    data_frame=df, x='Date', y='New Deaths', title='Daily New Deaths'
)
fig4 = px.line(
    data_frame=df, x='Date', y='Tests Completed', 
    title='Daily Tests Completed'
)
fig5 = px.line(
    data_frame=df, x='Date', y='Percent Positive', 
    title='Daily Percent Positive'
)
fig6 = px.pie(
    names=['Recovered', 'Deceased', 'Active'],
    values=[total_recovered, total_deaths, total_active], 
    title=f'Total Case Summary [{str(df["Date"].max())}]'
)
# fig7 = (
#     px.bar(
#         data_frame=df_regional,
#         x='total_cases',
#         y='reporting_phu',
#         orientation='h',
#         title=f'Total Case Regional Breakdown [{str(df["Date"].max())}]',
#         labels={
#             'total_cases': 'Total Cases',
#             'reporting_phu': 'Reporting PHU'
#         },
#         color='total_cases',
#         color_continuous_scale='Peach',
#         text='total_cases'
#     )
#     .update_traces(textposition='outside', texttemplate='%{text:.2s}')
# )
fig8 = (
    px.bar(
        data_frame=df_regional,
        x=0,
        y=df_regional.index.tolist(),
        orientation='h',
        title=f'New Case Regional Breakdown [{str(df["Date"].max())}]',
        labels={
            'total_cases': 'New Cases',
            'y': 'Reporting PHU'
        }, 
        color=0,
        color_continuous_scale='Peach',
        text=0,
    )   
    .update_traces(textposition='outside')
)

figs_list = [fig1, fig2, fig3, fig4, fig5, fig8]
for i in figs_list:
    i.update_layout(
        yaxis=dict(fixedrange=True), xaxis=dict(fixedrange=True), 
        showlegend=False, margin={'r': 30}, coloraxis_showscale=False, 
        transition_duration=500,
    ) 

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
                            id='box1',
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
                            id='box2'
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
                            id='box3'
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
                            id='box4'
                        ),
                    ],

                    id='info-container',
                    className='container-display',
                )
            ]
        ),

        # Store the fig dictionaries for user in callbacks
        dcc.Store(
            id='clientside_datastore',
            data=figs_list[0:5]
        ),

        dcc.Store(
            id='clientside_datastore2',
            data=None
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
                            id='datepicker_output',
                        ),

                        html.Div(
                            [
                                html.Button(
                                    'Reset',
                                    id='reset_graphs_button',
                                    n_clicks=0
                                )
                            ],
                            id='reset_button_div',
                            style={
                                'margin-left': 'auto',
                            }
                        )
                    ],
                    id='datepicker_bar',
                    className='mini_container',
                    style={
                        'display': 'flex',
                        'align-items': 'center',
                        'position': 'sticky',
                        'top': '0'
                    }
                ),
            ],
            className='container-display',
            id='datepicker_container',
            style={
                'position': 'sticky',
                'z-index': 1000
            }
        ),

        html.Div(
            [
                dcc.Graph(
                    figure=fig1, 
                    id='graph1', 
                    config={'displayModeBar': False,}
                ),
            ],

            className='pretty_container',
        ),

        html.Div(
            [
                dcc.Graph(
                    figure=fig8, 
                    id='graph8',
                    responsive=True, 
                    config={'displayModeBar': False,}
                ),
            ],

            className='pretty_container',
        ),
        
        html.Div(
            [
                dcc.Graph(
                    figure=fig3, 
                    id='graph3',
                    config={'displayModeBar': False,}
                ),
            ],

            className='pretty_container'
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            figure=fig4, 
                            id='graph4', 
                            config={'displayModeBar': False,}
                        ),
                    ],

                    className='pretty_container half_graph',
                ),

                html.Div(
                    [
                        dcc.Graph(
                            figure=fig5, 
                            id='graph5', 
                            config={'displayModeBar': False,}
                        ),
                    ],

                    className='pretty_container half_graph',
                    style={
                        # 'width' : '50%',
                    }
                ),
            ],
            className='two_graph_container',
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            figure=fig2, 
                            id='graph2', 
                            config={'displayModeBar': False,}
                        ),
                    ],

                    className='pretty_container half_graph',
                ),

                html.Div(
                    [
                        dcc.Graph(
                            figure=fig6, 
                            id='graph6', 
                            config={'displayModeBar': False,}
                        ),
                    ],

                    className='pretty_container half_graph',
                ),
            ],
            className='two_graph_container'
        ),
        
        # html.Div(
        #     [
        #         dcc.Graph(
        #             figure=fig7, 
        #             id='graph7', 
        #             config={'displayModeBar': False,}
        #         ),
        #     ],

        #     className='pretty_container',
        # ),

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

                html.P(
                    f'Last updated {df["Date"].max()}',
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

# Using clientside callbacks to avoid "expensive" serverside callbacks
# - Callbacks are executed when changes occur to the state of the Input
#   Ex. when prop 'n_clicks' of element with id 'reset_graphs_button' changes,
#   execute the callback

# Reset daterange button -> datepicker
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='reset_daterange'
    ),
    [
        Output('datepicker', 'start_date'),
        Output('datepicker', 'end_date'),
    ],
    [
        Input('reset_graphs_button', 'n_clicks'),
    ]
)

# datepicker -> clientside_datastore2, datepicker output message
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_daterange',
    ),
    [
        Output('datepicker_output', 'children'), 
        Output('clientside_datastore2', 'data'),
    ],
    [
        Input('datepicker', 'start_date'),
        Input('datepicker', 'end_date'),
    ]
)

# clientside_datastore2 -> graphs
# - Update graphs by mutating figure dictionaries stored in variable
#   clientside_datastore 
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_graphs'
    ),
    [
        Output('graph1', 'figure'), 
        Output('graph2', 'figure'), 
        Output('graph3', 'figure'), 
        Output('graph4', 'figure'), 
        Output('graph5', 'figure'), 
    ],
    [
        Input('clientside_datastore', 'data'),
        Input('clientside_datastore2', 'data'),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
