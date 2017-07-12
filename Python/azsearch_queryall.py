"""
Python code to retrieve batch answers from Azure Search

Run this script in the 'code' directory:
    python azsearch_queryall.py

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
import pyexcel as pe
import codecs
import pandas as pd

# Index gets created
#indexName = 'mh-eyfulltaxidxer'  # index of all 51 chapters, fixed H3 sub-subsections
indexName = 'mh-eytaxidxer'      # index of chapters 5-12, keywords + paratext + titles, fixed H3

# This is the service you've already created in Azure Portal
serviceName = 'eyazuresearch2017'

# Other globals
#apiKey = os.getenv('SEARCH_KEY_DEV', '')
apiKey = '8F36AE0F57D714CDDEC62EC79C6D5FF1'
apiVersion = '2016-09-01'

# Input file must be .xls (not .xlsx)
INDIR = './hackfest'
infile  = INDIR + '/700-for-MS-questions.xlsx'

# Number of results to return
NTOP = 5
OUT_TXT   = INDIR + '/MS-azanswers-%s-top%d.txt'  % (indexName, NTOP)
#OUT_EXCEL = INDIR + '/MS-azanswers-%s-top%d.xlsx' % (indexName, NTOP)

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
    #print(r, r.text)
    docs = json.loads(r.text)['value']
    return docs

#######################################################
# Retrieve Azure Search documents for all questions
# Fields: Index	File	Chapter	Title	SectionTitle	SubsectionTitle	Source	FeatureType	ParaText	Keywords
#######################################################
if __name__ == '__main__':
    # Dataframe to keep index of crawled pages
    df = pd.DataFrame(columns = ['Qid', 'Question', 'Rank', 'Answer', 'Chapter', 'Title', 'Section', 'Subsection', 'Source', 'FeatureType', 'Keywords'], dtype=unicode)

    records = pe.iget_records(file_name=infile)
    for row in records:
        qid   = int(row['Qid'])
        query = row['Question']
        # Submit query to Azure Search and retrieve results
        #searchFields = None
        searchFields = 'Keywords, ParaText'
        docs = submitQuery(query, fields=searchFields, ntop=NTOP)
        print('QID: %4d\tNumber of results: %d' % (qid, len(docs)))
        for id, doc in enumerate(docs):
            chapter    = doc['Chapter']
            title      = doc['Title']
            section    = doc['SectionTitle']
            subsection = doc['SubsectionTitle']
            source     = doc['Source']
            feature    = doc['FeatureType']
            paratext   = doc['ParaText'].encode('utf8')
            keywords   = doc['Keywords'].encode('utf8')

            df = df.append({'Qid'        : qid, 
                            'Question'   : query, 
                            'Rank'       : (id + 1), 
                            'Answer'     : paratext,
                            'Chapter'    : chapter,
                            'Title'      : title,
                            'Section'    : section,
                            'Subsection' : subsection,
                            'Source'     : source,
                            'FeatureType': feature,
                            'Keywords'   : keywords},
                            ignore_index=True)

    # Save all answers
    df['Qid']  = df['Qid'].astype(int)
    df['Rank'] = df['Rank'].astype(int)
    df.to_csv(OUT_TXT, sep='\t', index=False, encoding='utf-8')    
    #df.to_excel(OUT_EXCEL, index=False, encoding='utf-8')    

