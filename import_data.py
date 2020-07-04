'''----------------------------------------------------------------------------
Name:        Import Data Command (import_data.py)
Purpose:     To import data into the database. SHOULD ONLY BE USED ON A NEWLY
             CREATED SQLITE DATABASE FILE. Script queries all data from the 
             Government of Ontario's API, then saves to the local database 
             (database.db)

Author:      Nicholas Chong
Created:     2020-06-23 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import urllib.request
import pprint
import json
from models import *
import datetime

def main():
    # Connect to the Ontario Government API
    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=1000'
    query = urllib.request.urlopen(link)
    query = json.loads(query.read()).

    # Get data from API call
    for count, report in enumerate(query['result']['records']):
        # Get required data and store in variables
        date = datetime.datetime.strptime(report['Reported Date'][0:10], "%Y-%m-%d").date()
        net_new_tests = report['Total tests completed in the last day']
        total_cases = report['Total Cases']
        total_deaths = report['Deaths']

        if report['_id'] != 1:
            past_day = query['result']['records'][count-1]
            try:
                net_new_cases = report['Total Cases'] - past_day['Total Cases']
            except:
                net_new_cases = 0

            try:
                net_new_deaths = report['Deaths'] - past_day['Deaths']
            except:
                net_new_deaths = 0

            print(report['_id'], net_new_deaths, net_new_cases)
        else:
            net_new_cases = 0
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
    main()