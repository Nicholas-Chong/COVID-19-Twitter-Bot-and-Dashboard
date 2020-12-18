'''----------------------------------------------------------------------------
Name:        Update Data Command (update_data.py)
Purpose:     Used to query new data from the Government of Ontario's API, 
             Format it appropriately, and add it to the local database 
             (database.db)

Author:      Nicholas Chong
Created:     2020-06-23 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import urllib.request
import pprint
import json
from .models import *
import datetime

def update():
    # Get today's date -> Convert it into a string
    todaysdate = str(
        Daily_Report
        .select()
        .order_by(Daily_Report.id.desc())
        .get().date+datetime.timedelta(days=1)
    )

    # Access Ontario Government coronavirus API; Search by today's date
    link = f'https://data.ontario.ca/api/3/action/datastore_search?q={todaysdate}&resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11'
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())

    sort_function = (
        lambda x: 
        datetime.datetime.strptime(x['Reported Date'][0:10], "%Y-%m-%d").date()
    )
    sorted_query = sorted(
        query['result']['records'], 
        key=sort_function, 
        reverse=True
    )

    # Isolate today's record and print
    report = sorted_query[0]

    # Get required data, format and store in variables
    date = (
        datetime.datetime
        .strptime(report['Reported Date'][0:10], "%Y-%m-%d")
        .date()
    )

    if str(todaysdate) != str(date):
        return print('DATASET HAS NOT UPDATED')

    net_new_tests = report['Total tests completed in the last day']
    total_cases = report['Total Cases']
    total_deaths = report['Deaths']
    total_recovered = report['Resolved']

    # Query the last row in the database
    past_day = Daily_Report.select().order_by(Daily_Report.id.desc()).get()

    # Get net increases in net_new_cases and net_new_deaths
    try:
        net_new_cases = report['Total Cases'] - past_day.total_cases
    except:
        net_new_cases = 0

    try:
        net_new_deaths = report['Deaths'] - past_day.total_deaths
    except:
        net_new_deaths = 0

    # Create a new Daily_Report and add into database
    Daily_Report.create(
        date=date,
        net_new_cases=net_new_cases,
        net_new_tests= net_new_tests,
        net_new_deaths=net_new_deaths,
        total_cases=total_cases,
        total_deaths=total_deaths,
        total_resolved=total_recovered,
    )


def regional_update():
    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=8a88fe6d-d8fb-41a3-9d04-f0550a44999f&limit=10000'
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())

    sort_function = (
        lambda x: 
        datetime.datetime.strptime(x['Date'][0:10], "%Y-%m-%d").date()
    )
    sorted_query = sorted(
        query['result']['records'], 
        key=sort_function, 
        reverse=True
    )
    
    Daily_Regional_Report.create(
        Date = sorted_query[0]['Date'],
        Algoma_Public_Health_Unit = sorted_query[0]['Algoma_Public_Health_Unit'],
        Brant_County_Health_Unit = sorted_query[0]['Brant_County_Health_Unit'],
        Chatham_Kent_Health_Unit = sorted_query[0]['Chatham-Kent_Health_Unit'],
        Durham_Region_Health_Department = sorted_query[0]['Durham_Region_Health_Department'],
        Eastern_Ontario_Health_Unit = sorted_query[0]['Eastern_Ontario_Health_Unit'],
        Grey_Bruce_Health_Unit = sorted_query[0]['Grey_Bruce_Health_Unit'],
        Haldimand_Norfolk_Health_Unit = sorted_query[0]['Haldimand-Norfolk_Health_Unit'],
        Haliburton_Kawartha_Pine_Ridge_District_Health_Unit = sorted_query[0]['Haliburton,_Kawartha,_Pine_Ridge_District_Health_Unit'],
        Halton_Region_Health_Department = sorted_query[0]['Halton_Region_Health_Department'],
        Hamilton_Public_Health_Services = sorted_query[0]['Hamilton_Public_Health_Services'],
        Hastings_and_Prince_Edward_Counties_Health_Unit = sorted_query[0]['Hastings_and_Prince_Edward_Counties_Health_Unit'],
        Huron_Perth_District_Health_Unit = sorted_query[0]['Huron_Perth_District_Health_Unit'],
        Kingston_Frontenac_and_Lennox_and_Addington_Public_Health = sorted_query[0]['Kingston,_Frontenac_and_Lennox_&_Addington_Public_Health'],
        Lambton_Public_Health = sorted_query[0]['Lambton_Public_Health'],
        Leeds_Grenville_and_Lanark_District_Health_Unit = sorted_query[0]['Leeds,_Grenville_and_Lanark_District_Health_Unit'],
        Middlesex_London_Health_Unit = sorted_query[0]['Middlesex-London_Health_Unit'],
        Niagara_Region_Public_Health_Department = sorted_query[0]['Niagara_Region_Public_Health_Department'],
        North_Bay_Parry_Sound_District_Health_Unit = sorted_query[0]['North_Bay_Parry_Sound_District_Health_Unit'],
        Northwestern_Health_Unit = sorted_query[0]['Northwestern_Health_Unit'],
        Ottawa_Public_Health = sorted_query[0]['Ottawa_Public_Health'],
        Peel_Public_Health = sorted_query[0]['Peel_Public_Health'],
        Peterborough_Public_Health = sorted_query[0]['Peterborough_Public_Health'],
        Porcupine_Health_Unit = sorted_query[0]['Porcupine_Health_Unit'],
        Region_of_WaterlooPublic_Health = sorted_query[0]['Region_of_Waterloo,_Public_Health'],
        Renfrew_County_and_District_Health_Unit = sorted_query[0]['Renfrew_County_and_District_Health_Unit'],
        Simcoe_Muskoka_District_Health_Unit = sorted_query[0]['Simcoe_Muskoka_District_Health_Unit'],
        Southwestern_Public_Health = sorted_query[0]['Southwestern_Public_Health'],
        Sudbury_and_District_Health_Unit = sorted_query[0]['Sudbury_&_District_Health_Unit'],
        Thunder_Bay_District_Health_Unit = sorted_query[0]['Thunder_Bay_District_Health_Unit'],
        Timiskaming_Health_Unit = sorted_query[0]['Timiskaming_Health_Unit'],
        Toronto_Public_Health = sorted_query[0]['Toronto_Public_Health'],
        Wellington_Dufferin_Guelph_Public_Health = sorted_query[0]['Wellington-Dufferin-Guelph_Public_Health'],
        Windsor_Essex_County_Health_Unit = sorted_query[0]['Windsor-Essex_County_Health_Unit'],
        York_Region_Public_Health_Services = sorted_query[0]['York_Region_Public_Health_Services'],
    )
