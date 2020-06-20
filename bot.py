'''
This script links to the Status of COVID-19 cases in Ontario API provided by 
the Ontario government.

The API provides Compiled daily reported data on COVID-19 testing and outcomes 
in Ontario.
'''

import urllib.request
import pprint
import json
import graphs
import tweets

def main():
    link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=1000'

    query = urllib.request.urlopen(link)
    query = json.loads(query.read())
    # pprint.pprint(query['result']['records'])

    results = query['result']['records']
    num_results = len(results) - 1

    date = results[num_results]['Reported Date'][0:10]

    new_cases = results[num_results]['Total Cases'] - results[num_results - 1]['Total Cases']
    print(new_cases)

    tests_completed = results[num_results]['Total tests completed in the last day']
    
    total_cases = results[num_results]['Total Cases'] 
    # print(total_cases) 

    new_cases_data = [(i['_id'], i['Total Cases']) for i in results]
    # print(new_cases_data)

    graphs.total_case_chart(new_cases_data)

    tweets.daily_update(
        date, 
        new_cases, 
        total_cases,
        tests_completed,
    )

if __name__ == '__main__':
    main()
