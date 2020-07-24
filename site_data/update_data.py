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
    date = str(datetime.datetime.now().date())
    print(date)

    # Access Ontario Government coronavirus API; Search by today's date
    link = f'https://data.ontario.ca/api/3/action/datastore_search?q={date}&resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11'
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())

    sort_function = lambda x: datetime.datetime.strptime(x['Reported Date'][0:10], "%Y-%m-%d").date()
    sorted_query = sorted(
        query['result']['records'], 
        key=sort_function, 
        reverse=True
        )
    pprint.pprint(sorted_query)

    # Isolate today's record and print
    report = sorted_query[0]
    pprint.pprint(report)

    # Get required data, format and store in variables
    date = datetime.datetime.strptime(report['Reported Date'][0:10], "%Y-%m-%d").date() # Convert datetime string into date object
    net_new_tests = report['Total tests completed in the last day']
    total_cases = report['Total Cases']
    total_deaths = report['Deaths']

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
    )


if __name__ == '__main__':
    update()