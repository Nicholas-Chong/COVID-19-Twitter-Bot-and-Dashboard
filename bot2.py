'''
This script links to the Confirmed positive cases of COVID19 in Ontario 
database provided by the government.

This dataset compiles daily snapshots of publicly reported data on 2019 Novel 
Coronavirus (COVID-19) testing in Ontario.
'''

import urllib.request
import pprint
import json

link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=455fd63b-603d-4608-8216-7d8647f43350&limit=1000000'

query = urllib.request.urlopen(link)
query = json.loads(query.read())

print(len(query['result']['records']))

count = 0
for i in query['result']['records']:
    if i['Case_Reported_Date'] in ['2020-06-18T00:00:00']:
        count += 1
        print(f"{count} {i['Reporting_PHU_City']}")

print(count)
# pprint.pprint(query['result']['records'])
