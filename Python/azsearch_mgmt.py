"""
Python code to upload data to Azure Search for the MLADS Bot.

This script will upload all of the session information where
each individual sesssion equates to a document in an index
in an Azure Search service.

Go to http://portal.azure.com and sign up for a search service.
Get the service name and service key and plug it in below.
This is NOT production level code. Please do not use it as such.
You might have to pip install the imported modules here.

Run this script in the 'code' directory:
    python search_mgmt.py

See Azure Search REST API docs for more info:
    https://docs.microsoft.com/en-us/rest/api/searchservice/index

"""

import requests
import json
import csv
import datetime
import calendar
import os
import pyexcel as pe


# Index gets created
#indexName = 'mh-eyfulltaxidxer'
indexName = 'mh-eytaxidxer'

# This is the service you've already created in Azure Portal
serviceName = 'eyazuresearch2017'

# Other globals
#apiKey = os.getenv('SEARCH_KEY_DEV', '')
apiKey = '8F36AE0F57D714CDDEC62EC79C6D5FF1'
apiVersion = '2015-02-28-Preview'

# Input file must be .xls (not .xlsx)
#inputfile = os.path.join(os.getcwd(), './parsed/ms_parsed_h3_full_tax_guide_keywords.xlsx')
inputfile = os.path.join(os.getcwd(), './parsed/ms_parsed_h3_tax_guide_keywords.xlsx')

def getSampleDocumentObject():
    valarry = []
    cnt = 1
    records = pe.iget_records(file_name=inputfile)
    for row in records:
        outdict = {}
        outdict['@search.action'] = 'upload'

        if (row['Title']):
            outdict['Index']           = str(row['Index'])
            outdict['File']            = row['File']
            outdict['Chapter']         = row['Chapter']
            outdict['Title']           = row['Title']
            outdict['SectionTitle']    = row['SectionTitle']
            outdict['SubsectionTitle'] = row['SubsectionTitle']
            outdict['Source']          = row['Source']
            outdict['FeatureType']     = row['FeatureType']
            outdict['ParaText']        = row['ParaText']
            outdict['Keywords']        = row['Keywords']
        valarry.append(outdict)
        cnt+=1

    return {'value' : valarry}

def getSampleDocumentObjectByChunk(start, end):
    valarry = []
    cnt = 1
    records = pe.iget_records(file_name=inputfile)
    for i, row in enumerate(records):
        if start <= i < end:
            outdict = {}
            outdict['@search.action'] = 'upload'

            if (row['Title']):
                outdict['Index']           = str(row['Index'])
                outdict['File']            = row['File']
                outdict['Chapter']         = row['Chapter']
                outdict['Title']           = row['Title']
                outdict['SectionTitle']    = row['SectionTitle']
                outdict['SubsectionTitle'] = row['SubsectionTitle']
                outdict['Source']          = row['Source']
                outdict['FeatureType']     = row['FeatureType']
                outdict['ParaText']        = row['ParaText']
                outdict['Keywords']        = row['Keywords']
            valarry.append(outdict)
            cnt+=1

    return {'value' : valarry}

# Fields: Index	File	Chapter	Title	SectionTitle	SubsectionTitle	Source	FeatureType	ParaText	Keywords
def getSampleIndexDefinition():
    return {
    "name": indexName,
    "fields":
    [
        {
            "name": "Index",
            "type": "Edm.String",
            "searchable": False,
            "filterable": False,
            "retrievable": True,
            "sortable": True,
            "facetable": False,
            "key": True,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
            "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "File",
            "type": "Edm.String",
            "searchable": False,
            "filterable": True,
            "retrievable": True,
            "sortable": True,
            "facetable": False,
            "key": False,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
            "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "Chapter",
            "type": "Edm.String",
            "searchable": False,
            "filterable": True,
            "retrievable": True,
            "sortable": True,
            "facetable": False,
            "key": False,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
            "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "Title",
            "type": "Edm.String",
            "searchable": True,
            "filterable": True,
            "retrievable": True,
            "sortable": True,
            "facetable": True,
            "key": False,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
           "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "SectionTitle",
            "type": "Edm.String",
            "searchable": True,
            "filterable": True,
            "retrievable": True,
            "sortable": False,
            "facetable": True,
            "key": False,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
            "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "SubsectionTitle",
            "type": "Edm.String",
            "searchable": True,
            "filterable": True,
            "retrievable": True,
            "sortable": True,
            "facetable": False,
            "key": False,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
            "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "Source",
            "type": "Edm.String",
            "searchable": False,
            "filterable": False,
            "retrievable": True,
            "sortable": True,
            "facetable": True,
            "key": False,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
            "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "FeatureType",
            "type": "Edm.String",
            "searchable": False,
            "filterable": True,
            "retrievable": True,
            "sortable": True,
            "facetable": True,
            "key": False,
            "indexAnalyzer": None,
            "searchAnalyzer": None,
            "analyzer": None,
            "synonymMaps": []
        },
        {
            "name": "ParaText",
            "type": "Edm.String",
            "searchable": True,
            "filterable": False,
            "retrievable": True,
            "sortable": False,
            "facetable": False,
            "key": False,
      "indexAnalyzer": "english_indexing_analyzer",
      "searchAnalyzer": "english_search_analyzer",
            "synonymMaps": []
        },
        {
            "name": "Keywords",
            "type": "Edm.String",
            "searchable": True,
            "filterable": False,
            "retrievable": True,
            "sortable": False,
            "facetable": False,
            "key": False,
      "indexAnalyzer": "english_indexing_analyzer",
      "searchAnalyzer": "english_search_analyzer",
            "synonymMaps": []
       }
    ],
  "scoringProfiles": [
    {
      "name": "boostexperiment",
      "text": {

        "weights": {

          "Title": 1,

          "Keywords": 1
        }
      }
    }
],


  "analyzers": [
    {
      "@odata.type": "#Microsoft.Azure.Search.CustomAnalyzer",
      "name": "english_search_analyzer",
      "tokenizer": "english_search",
      "tokenFilters": [
        "lowercase"
      ],
      "charFilters": ["form_suffix"]
    },
    {
      "@odata.type": "#Microsoft.Azure.Search.CustomAnalyzer",
      "name": "english_indexing_analyzer",
      "tokenizer": "english_indexing",
      "tokenFilters": [
        "lowercase"
      ],
      "charFilters": ["form_suffix"]
    }
  ],
  "tokenizers": [
    {
      "@odata.type": "#Microsoft.Azure.Search.MicrosoftLanguageStemmingTokenizer",
      "name": "english_indexing",
      "language": "english",
      "isSearchTokenizer": False
    },
    {
      "@odata.type": "#Microsoft.Azure.Search.MicrosoftLanguageStemmingTokenizer",
      "name": "english_search",
      "language": "english",
      "isSearchTokenizer": False
    }
  ],
  "tokenFilters": [],
  "charFilters": [
     {
       "name":"form_suffix",
       "@odata.type":"#Microsoft.Azure.Search.PatternReplaceCharFilter",
       "pattern":"([0-9]{4})-([A-Z]*)",
       "replacement":"$1$2"
     }
  ]
}


def getServiceUrl():
    return 'https://' + serviceName + '.search.windows.net'

def getMethod(servicePath):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.get(getServiceUrl() + servicePath, headers=headers)
    print(r.text)

def postMethod(servicePath, body):
    headers = {'Content-type': 'application/json', 'api-key': apiKey}
    r = requests.post(getServiceUrl() + servicePath, headers=headers, data=body)
    #print(r, r.text)
    return r

def createSampleIndex():
    indexDefinition = json.dumps(getSampleIndexDefinition())
    servicePath = '/indexes/?api-version=%s' % apiVersion
    r = postMethod(servicePath, indexDefinition)
    #print r.text
    if r.status_code == 201:
       print('Sample index created.')
    else:
       print('Sample index creation failed.')
       exit(1)

def getSampleIndex():
    #servicePath = '/indexers/%s?api-version=%s' % (indexName, apiVersion)
    servicePath = '/indexers/?api-version=%s' % (apiVersion)
    getMethod(servicePath)

def uploadSampleDocument():
    documents = json.dumps(getSampleDocumentObject())
    servicePath = '/indexes/' + indexName + '/docs/index?api-version=' + apiVersion
    r = postMethod(servicePath, documents)
    if r.status_code == 200:
        print('Success: %s' % r)
    else:
        print('Failure: %s' % r.text)

def uploadSampleDocumentInChunks(chunksize):
    records = pe.iget_records(file_name=inputfile)
    cnt  = 0
    for row in records:
        cnt += 1
    #chunksize = 50
    #for chunk in [65, 68, 72]:   # these chunks of size 50 fail to load
    for chunk in range(cnt/chunksize + 1):
        print('Processing chunk number %d ...' % chunk)
        start = chunk * chunksize
        end   = start + chunksize
        documents = json.dumps(getSampleDocumentObjectByChunk(start, end))
        servicePath = '/indexes/' + indexName + '/docs/index?api-version=' + apiVersion
        r = postMethod(servicePath, documents)
        if r.status_code == 200:
            print('Success: %s' % r)
        else:
            print('Failure: %s' % r.text)

def uploadSampleDocumentOneByOne():
    records = pe.iget_records(file_name=inputfile)
    valarry = []
    for i, row in enumerate(records):
        outdict = {}
        outdict['@search.action'] = 'upload'

        if (row['Title']):
            outdict['Index']           = str(row['Index'])
            outdict['File']            = row['File']
            outdict['Chapter']         = row['Chapter']
            outdict['Title']           = row['Title']
            outdict['SectionTitle']    = row['SectionTitle']
            outdict['SubsectionTitle'] = row['SubsectionTitle']
            outdict['Source']          = row['Source']
            outdict['FeatureType']     = row['FeatureType']
            outdict['ParaText']        = row['ParaText']
            outdict['Keywords']        = row['Keywords']
            valarry.append(outdict)

        documents = json.dumps({'value' : valarry})
        servicePath = '/indexes/' + indexName + '/docs/index?api-version=' + apiVersion
        r = postMethod(servicePath, documents)
        if r.status_code == 200:
            print('%d Success: %s' % (i,r))
        else:
            print('%d Failure: %s' % (i, r.text))

def printDocumentCount():
    servicePath = '/indexes/' + indexName + '/docs/$count?api-version=' + apiVersion
    getMethod(servicePath)

def sampleQuery(query):
    servicePath = '/indexes/' + indexName + '/docs?search=%s&api-version=%s' % \
        (query, apiVersion)
    getMethod(servicePath)


if __name__ == '__main__':
    # createSampleIndex()
    # getSampleIndex()
    # uploadSampleDocument()
    uploadSampleDocumentInChunks(50)
    # uploadSampleDocumentOneByOne()
    printDocumentCount()
    # sampleQuery('child tax credit')
