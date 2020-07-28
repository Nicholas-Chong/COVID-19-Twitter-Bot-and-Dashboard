'''----------------------------------------------------------------------------
Name:        Twitter Bot (bot.py)
Purpose:     A script that sends out a tweet containing general coronavirus 
             statistics from the Government of Ontario. Script is called 
             through heroku scheduler at 11:00AM every day.

Author:      Nicholas Chong
Created:     2020-06-19 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import urllib.request
import pprint
import json
from . import tweets 

def main():
    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=1000'

    # Query data through API
    query = urllib.request.urlopen(link)
    query = json.loads(query.read())

    results = query['result']['records']
    num_results = len(results) - 1

    # Isolate required data and store in variables
    date = results[num_results]['Reported Date'][0:10]
    new_cases = results[num_results]['Total Cases'] - results[num_results - 1]['Total Cases']
    tests_completed = results[num_results]['Total tests completed in the last day']
    total_cases = results[num_results]['Total Cases'] 

    # Send out the daily update tweet
    tweets.daily_update(
        date, 
        new_cases, 
        total_cases,
        tests_completed,
    )

    print(True)
if __name__ == '__main__':
    main()
