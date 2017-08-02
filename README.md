
# Custom Search 

> Sample custom search project using azure search and the US Tax Code.

> Python script that allows you to quickly and iteratively customize, improve and measure your custom search experience.


## Custom Search Service Development Features in the Python Scripts 
* Upload and update search index in Azure Search 
* Query interactively to test results 
* Query on batch basis to analyze performance
* Extract keyphrases to enhance search index metadata 


## Getting Started

1. Read the [Real Life Code Story](https://www.microsoft.com/reallifecode/), "[Developing a Custom Search Engine for an Expert Chat System.](https://www.microsoft.com/reallifecode/)"
https://github.com/CatalystCode/CustomSearch/blob/master/Python/azsearch_queryall.py
2. Review the [Azure Search service features](https://azure.microsoft.com/en-us/services/search/).
3. Get a [free trial subscriptions to Azure Search.](https://azure.microsoft.com/en-us/free/)
4. Copy your Azure Search name and Key. 
5. Review the [sample](https://github.com/CatalystCode/CustomSearch/tree/master/sample)
 search index input and enriched input in the sample folder to understand content.
6. Run the [azsearch_mgmt.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/azsearch_mgmt.py), using your Azure Search name, key and index name of your choice to create a search index.
7. Run the [azsearch_query.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/azsearch_query.py) to interactively query your new search index and see results.
8. Run the [azsearch_queryall.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/azsearch_queryall.py) to batch query your new search index and evaluate the results.
9. Run the [keyphrase_extract.py script](https://github.com/CatalystCode/CustomSearch/blob/master/Python/keyphrase_extract.py) to extract keyphrases to enrich the search index metadata.  Note this script is Python 2.7 only.

 
## Description
Querying specific content areas quickly and easily is a common enterprise need. Fast traversal of specialized publications, customer support knowledge bases or document repositories allows enterprises to deliver service efficiently and effectively. Simple FAQs don’t cover enough ground, and a string search isn’t effective or efficient for those not familiar with the domain or the document set. Instead, enterprises can deliver a custom search experience that saves their clients time and provides them better service through a question and answer format.  In this project, we leveraged Azure Search and Cognitive Services and we share our custom code for iterative testing, measurement and indexer redeployment. In our solution, the customized search engine will form the foundation for delivering a question and answer experience in a specific domain area.
