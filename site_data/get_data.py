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

### DAILY ONTARIO DATA ###

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

# Sort by date to ensure everything is in the correct order
df = df.sort_values(by=['Date'])

# Determine 7 day rolling average
df['7 Day Average'] = df['New Cases'].rolling(window=7).mean()

# Determine daily percent positive
df['Percent Positive'] = round((df['New Cases']/df['Tests Completed'])*100, 2)

# Store day over day increases in lists
dod_new_cases = day_over_day(
    df.iloc[-1]['New Cases'], 
    df.iloc[-2]['New Cases']
)
dod_new_deaths = day_over_day(
    df.iloc[-1]['New Deaths'], 
    df.iloc[-2]['New Deaths']
)

### DAILY REGIONAL DATA ###

# Query most recent regional data and return as dict
most_recent_regional = Daily_Regional_Report.select(fn.MAX(Daily_Regional_Report.Date)).scalar()
regional_data = Daily_Regional_Report.select().where(Daily_Regional_Report.Date == most_recent_regional).dicts()
df_regional = pd.DataFrame(regional_data).drop(columns=['id', 'Date'])
df_regional = df_regional.rename(columns={'Kingston_Frontenac_and_Lennox_and_Addington_Public_Health': 'Kingston-Frontenac,Lennox-Addington'})
df_regional = df_regional.iloc[0]
df_regional = df_regional.sort_values()

### Pie Graph Data ###
total_recovered = df.at[len(df)-1, 'Total Recovered'],
total_deaths = df.at[len(df)-1, 'Total Deaths'],
total_active = df.at[len(df)-1, 'Total Cases'] - total_recovered - total_deaths

### VACCINATION DATA ###
vaccination_data = Daily_Vacination.select().dicts()
vaccination_data = pd.DataFrame(vaccination_data).drop(columns=['id'])