"""
Python code to query Azure Search interactively

Run this script in the 'code' directory:
    python azsearch_query.py

See Azure Search REST API docs for more info:
    https://docs.microsoft.com/en-us/rest/api/searchservice/index

"""

import requests
import json
import csv
import datetime
import pytz
import calendar
import os

# Index gets created
#indexName = 'mh-eyfulltaxidxer'  # index of all 51 chapters, fixed H3 sub-subsections
indexName = 'mh-eytaxidxer'      # index of chapters 5-12, keywords + paratext + titles, fixed H3

# This is the service you've already created in Azure Portal
serviceName = 'eyazuresearch2017'

# Other globals
#apiKey = os.getenv('SEARCH_KEY_DEV', '')
apiKey = '8F36AE0F57D714CDDEC62EC79C6D5FF1'
apiVersion = '2016-09-01'

def getServiceUrl():
    return 'https://' + serviceName + '.search.windows.net'

def getMethod(servicePath):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.get(getServiceUrl() + servicePath, headers=headers)
    #print(r, r.text)
    return r

def postMethod(servicePath, body):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.post(getServiceUrl() + servicePath, headers=headers, data=body)
    #print(r, r.text)
    return r

def submitQuery(query, fields=None, ntop=10):
    servicePath = '/indexes/' + indexName + '/docs?api-version=%s&search=%s&$top=%d' % \
        (apiVersion, query, ntop)
    if fields != None:
        servicePath += '&searchFields=%s' % fields
    r = getMethod(servicePath)
    if r.status_code != 200:
        print('Failed to retrieve search results')
        print(r, r.text)
        return
    docs = json.loads(r.text)['value']
    print('Number of search results = %d' % len(docs))
    for i, doc in enumerate(docs):
        print('Result# %d (%s)' % (i+1, doc['Chapter']))
        print('%s\n' % doc['ParaText'].encode('utf8'))


#######################################################
# Retrieve Azure Search documents for interactive query
# Fields: Index	File	Chapter	Title	SectionTitle	SubsectionTitle	Source	FeatureType	ParaText	Keywords
#######################################################
if __name__ == '__main__':
    while True:
        print
        print "Hit enter with no input to quit."
        query = raw_input("Query: ")
        if query == '':
            exit(0)

        # Submit query to Azure Search and retrieve results
        #searchFields = None
        searchFields = 'Keywords, ParaText'
        submitQuery(query, fields=searchFields, ntop=3)