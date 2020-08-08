'''----------------------------------------------------------------------------
Name:        Get Data (get_data.py)
Purpose:     To query data from the database and transform into a usable pandas 
             dataframe. Dataframe will be used to present data in Plotly Dash.
             To be imported by dashboard.py .

Author:      Nicholas Chong
Created:     2020-07-21 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import plotly.express as px
import pandas as pd
from .models import * # Relative import (dashboard.py -> get_data.py)
from datetime import timedelta

# Function to get day over day variances; pass on the corresponding color
def day_over_day(today, yesterday):
    difference = today - yesterday
    if difference > 0:
        return [f'+{str(difference)} increase vs yesterday', 'orangered']
    else:
        return [f'{str(difference)} decrease vs yesterday', 'limegreen']

# Query data and return as dictionary
data = Daily_Report.select().dicts()

# Create pandas dataframe
df = pd.DataFrame({
    'Date' : [i['date'] for i in data],
    'New Cases' : [i['net_new_cases'] for i in data],
    'Total Cases' : [i['total_cases'] for i in data],
    'New Deaths' : [i['net_new_deaths'] for i in data],
    'Total Deaths' : [i['total_deaths'] for i in data],
    'Tests Completed' : [i['net_new_tests'] for i in data],
    'Total Recovered' : [i['total_resolved'] for i in data],
})

# Determine 7 day rolling average
df['7 Day Average'] = df['New Cases'].rolling(window=7).mean()

# Determine daily percent positive
df['Percent Positive'] = round((df['New Cases'] / df['Tests Completed']) * 100, 2)

# Store day over day increases in lists
dod_new_cases = day_over_day(df.iloc[-1]['New Cases'], df.iloc[-2]['New Cases'])
dod_new_deaths = day_over_day(df.iloc[-1]['New Deaths'], df.iloc[-2]['New Deaths'])

# Query regional data and return as dict
regional_data = Daily_Regional_Report.select().where(
    Daily_Regional_Report.date == df['Date'].max()-timedelta(days=1)).dicts()
df_regional = pd.DataFrame(regional_data).sort_values(by=['new_cases'])