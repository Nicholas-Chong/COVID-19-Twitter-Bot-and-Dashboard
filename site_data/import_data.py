'''----------------------------------------------------------------------------
Name:        Import Data Command (import_data.py)
Purpose:     To import data into the database. SHOULD ONLY BE USED ON A NEWLY
             CREATED DATABASE. Script queries all data from the Government of 
             Ontario's API, then saves to the database.

Author:      Nicholas Chong
Created:     2020-06-23 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import urllib.request
from pprint import pprint
import json
from models import *
import datetime

def main():
    # Connect to the Ontario Government API
    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=1000'
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())

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


def importVax():
    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=8a89caa9-511c-4568-af89-7f2174b4378c&limit=100'
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())

    pprint(query['result']['records'])

    for r in query['result']['records']:
        date = datetime.datetime.strptime(r['report_date'][0:10], "%Y-%m-%d").date()
        new_doses = r['previous_day_doses_administered'].replace(',', '')
        total_doses = r['total_doses_administered'].replace(',', '')

        if new_doses == '':
            new_doses = 0
        
        print(date, new_doses, total_doses)

        Daily_Vacination.create(
            date=date,
            new_doses=int(new_doses),
            total_doses=int(total_doses)
        )

if __name__ == '__main__':
    importVax()