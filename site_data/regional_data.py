import urllib.request
import pprint
import json
from models import *
import datetime

link = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=455fd63b-603d-4608-8216-7d8647f43350&limit=1000000'

query = urllib.request.urlopen(link)
query = json.loads(query.read())
query = query['result']['records']
query = list(filter(lambda x: x['Case_Reported_Date'] == '2020-08-06T00:00:00', query))

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

pprint.pprint(phus_dict)
    