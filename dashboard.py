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
import pandas as pd
from models import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Dash CSS
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Ontario Coronavirus Summary'

data = Daily_Report.select().dicts()
df = pd.DataFrame({
    'Date' : [i['date'] for i in data],
    'New Cases' : [i['net_new_cases'] for i in data],
    'Total Cases' : [i['total_cases'] for i in data],
    'New Deaths' : [i['net_new_deaths'] for i in data],
    'Total Deaths' : [i['total_deaths'] for i in data],
    'Tests Completed' : [i['net_new_tests'] for i in data],
})
df['7 Day Average'] = df['New Cases'].rolling(window=7).mean()

# Create Figures
fig1 = px.line(data_frame=df, x='Date', y=['New Cases', '7 Day Average'], title='Daily New Cases')
fig2 = px.line(data_frame=df, x='Date', y='Total Cases', title='Total Cases')
fig3 = px.line(data_frame=df, x='Date', y='New Deaths', title='Daily New Deaths')
fig4 = px.line(data_frame=df, x='Date', y='Tests Completed', title='Daily Tests Completed')

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
                                )
                            ],

                            id='wells',
                            className='mini_container',
                        ),

                        html.Div(
                            [
                                html.H6(
                                    df.iloc[-1]['New Deaths']
                                ), 
                                
                                html.P(
                                    f'New Deaths ({df.iloc[-1]["Date"]})'
                                )
                            ],

                            id='gas',
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

                            id='oil',
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

                            id='water',
                            className='mini_container',
                        ),
                    ],

                    id='info-container',
                    className='container-display',
                )
            ]
        ),  

        html.Div(
            [
                dcc.Graph(figure=fig1),
            ],

            className='pretty_container'
        ),

        html.Div(
            [
                dcc.Graph(figure=fig2),
            ],

            className='pretty_container'
        ),
        
        html.Div(
            [
                dcc.Graph(figure=fig3),
            ],

            className='pretty_container'
        ),

        html.Div(
            [
                dcc.Graph(figure=fig4),
            ],

            className='pretty_container'
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
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)