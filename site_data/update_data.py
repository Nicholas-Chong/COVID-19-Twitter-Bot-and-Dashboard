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
    date = str(
        Daily_Report
        .select()
        .order_by(Daily_Report.id.desc())
        .get().date+datetime.timedelta(days=1)
    )

    # Access Ontario Government coronavirus API; Search by today's date
    link = f'https://data.ontario.ca/api/3/action/datastore_search?q={date}&resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11'
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
    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=455fd63b-603d-4608-8216-7d8647f43350&limit=1000000'

    date = str(
        Daily_Report
        .select()
        .order_by(Daily_Report.id.desc())
        .get().date-datetime
        .timedelta(days=1)
    )
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())
    query = query['result']['records']

    if len(query) == 0:
        return 
    
    phus_dict = {
        'North Bay Parry Sound District Health Unit': 0, 
        'Ottawa Public Health': 0, 
        'Region of Waterloo, Public Health': 0, 
        'Peterborough Public Health': 0, 
        'Huron Perth District Health Unit': 0, 
        'Leeds, Grenville and Lanark District Health Unit': 0, 
        'Timiskaming Health Unit': 0, 
        'Peel Public Health': 0, 
        'Porcupine Health Unit': 0, 
        'Lambton Public Health': 0, 
        'York Region Public Health Services': 0, 
        'Hamilton Public Health Services': 0, 
        'Thunder Bay District Health Unit': 0, 
        'Haldimand-Norfolk Health Unit': 0, 
        'Hastings and Prince Edward Counties Health Unit': 0, 
        'Niagara Region Public Health Department': 0, 
        'Chatham-Kent Health Unit': 0, 
        'Brant County Health Unit': 0, 
        'Grey Bruce Health Unit': 0, 
        'Toronto Public Health': 0, 
        'Kingston, Frontenac and Lennox & Addington Public Health': 0, 
        'Halton Region Health Department': 0, 
        'Simcoe Muskoka District Health Unit': 0, 
        'Sudbury & District Health Unit': 0, 
        'Durham Region Health Department': 0, 
        'Southwestern Public Health': 0, 
        'Algoma Public Health Unit': 0, 
        'Middlesex-London Health Unit': 0,
        'Haliburton, Kawartha, Pine Ridge District Health Unit': 0, 
        'Northwestern Health Unit': 0, 
        'Windsor-Essex County Health Unit': 0, 
        'Wellington-Dufferin-Guelph Public Health': 0, 
        'Renfrew County and District Health Unit': 0, 
        'Eastern Ontario Health Unit': 0
    }

    for i in query:
        phus_dict[i['Reporting_PHU']] += 1

    for i in phus_dict:
        Daily_Regional_Report.create(
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date(),
            reporting_phu = i,
            total_cases = phus_dict[i],
        )
        