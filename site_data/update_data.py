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
import logging

def update():
    logging.info('Starting provincial update')

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
    try:
        report = todays_record
    except:
        return logging.error('Todays record was not found. Unable to complete daily update.')

    # Get required data, format and store in variables
    date = (
        datetime.datetime
        .strptime(report['Reported Date'][0:10], "%Y-%m-%d")
        .date()
    )

    if str(todaysdate) != str(date):
        return logging.error('Todays record was not found. Unable to complete daily update.')

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
    logging.info('Provincial update complete')


def regional_update():
    logging.info('Starting regional update')

    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=8a88fe6d-d8fb-41a3-9d04-f0550a44999f&limit=10000'
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())
    logging.info('Queried data')

    sort_function = (
        lambda x: 
        datetime.datetime.strptime(x['Date'][0:10], "%Y-%m-%d").date()
    )
    sorted_query = sorted(
        query['result']['records'], 
        key=sort_function, 
        reverse=True
    )

    most_recent_record = Daily_Regional_Report.select().order_by(Daily_Regional_Report.Date.desc()).get().Date
    
    if datetime.datetime.strptime(sorted_query[0]['Date'][0:10], "%Y-%m-%d").date() != most_recent_record + datetime.timedelta(days=1):
        return logging.error('Todays record was not found. Unable to complete daily update.')

    todays_record = sorted_query[0]

    Daily_Regional_Report.create(
        Date = todays_record['Date'],
        Algoma_Public_Health_Unit = todays_record['Algoma_Public_Health_Unit'],
        Brant_County_Health_Unit = todays_record['Brant_County_Health_Unit'],
        Chatham_Kent_Health_Unit = todays_record['Chatham-Kent_Health_Unit'],
        Durham_Region_Health_Department = todays_record['Durham_Region_Health_Department'],
        Eastern_Ontario_Health_Unit = todays_record['Eastern_Ontario_Health_Unit'],
        Grey_Bruce_Health_Unit = todays_record['Grey_Bruce_Health_Unit'],
        Haldimand_Norfolk_Health_Unit = todays_record['Haldimand-Norfolk_Health_Unit'],
        Haliburton_Kawartha_Pine_Ridge_District_Health_Unit = todays_record['Haliburton,_Kawartha,_Pine_Ridge_District_Health_Unit'],
        Halton_Region_Health_Department = todays_record['Halton_Region_Health_Department'],
        Hamilton_Public_Health_Services = todays_record['Hamilton_Public_Health_Services'],
        Hastings_and_Prince_Edward_Counties_Health_Unit = todays_record['Hastings_and_Prince_Edward_Counties_Health_Unit'],
        Huron_Perth_District_Health_Unit = todays_record['Huron_Perth_District_Health_Unit'],
        Kingston_Frontenac_and_Lennox_and_Addington_Public_Health = todays_record['Kingston,_Frontenac_and_Lennox_&_Addington_Public_Health'],
        Lambton_Public_Health = todays_record['Lambton_Public_Health'],
        Leeds_Grenville_and_Lanark_District_Health_Unit = todays_record['Leeds,_Grenville_and_Lanark_District_Health_Unit'],
        Middlesex_London_Health_Unit = todays_record['Middlesex-London_Health_Unit'],
        Niagara_Region_Public_Health_Department = todays_record['Niagara_Region_Public_Health_Department'],
        North_Bay_Parry_Sound_District_Health_Unit = todays_record['North_Bay_Parry_Sound_District_Health_Unit'],
        Northwestern_Health_Unit = todays_record['Northwestern_Health_Unit'],
        Ottawa_Public_Health = todays_record['Ottawa_Public_Health'],
        Peel_Public_Health = todays_record['Peel_Public_Health'],
        Peterborough_Public_Health = todays_record['Peterborough_Public_Health'],
        Porcupine_Health_Unit = todays_record['Porcupine_Health_Unit'],
        Region_of_WaterlooPublic_Health = todays_record['Region_of_Waterloo,_Public_Health'],
        Renfrew_County_and_District_Health_Unit = todays_record['Renfrew_County_and_District_Health_Unit'],
        Simcoe_Muskoka_District_Health_Unit = todays_record['Simcoe_Muskoka_District_Health_Unit'],
        Southwestern_Public_Health = todays_record['Southwestern_Public_Health'],
        Sudbury_and_District_Health_Unit = todays_record['Sudbury_&_District_Health_Unit'],
        Thunder_Bay_District_Health_Unit = todays_record['Thunder_Bay_District_Health_Unit'],
        Timiskaming_Health_Unit = todays_record['Timiskaming_Health_Unit'],
        Toronto_Public_Health = todays_record['Toronto_Public_Health'],
        Wellington_Dufferin_Guelph_Public_Health = todays_record['Wellington-Dufferin-Guelph_Public_Health'],
        Windsor_Essex_County_Health_Unit = todays_record['Windsor-Essex_County_Health_Unit'],
        York_Region_Public_Health_Services = todays_record['York_Region_Public_Health_Services'],
    )
    
    logging.info('Regional update complete')
