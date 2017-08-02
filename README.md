
## Custom Search 

> Sample custom search project using azure search and the US Tax Code.

> Python script that allows you to quickly and iteratively customize, improve and measure your custom search experience.

# Scripts Included
* Upload and update search index in Azure Search
* Query interactively to test results
* Query on batch basis to analyze performance
* Extract keywords to enhance search index metadata (python 2.7 only)


## Guides

### How to view a file<a name="file"></a>

1. Open the appbar [`...`](#toggleAppBar) and select `Open File`
2. __or__ open a .md/.markdown file from the filesystem
3. __or__ copy a text, URL, file to the clipboard and switch back to Markdownr

## The Challenge
Querying specific content areas quickly and easily is a common enterprise need. Fast traversal of specialized publications, customer support knowledge bases or document repositories allows enterprises to deliver service efficiently and effectively. Simple FAQs don’t cover enough ground, and a string search isn’t effective or efficient for those not familiar with the domain or the document set. Instead, enterprises can deliver a custom search experience that saves their clients time and provides them better service through a question and answer format.

Consumer search engines combine many sophisticated techniques in each step of the process, from augmenting query and answer content, to indexing target content, to retrieval ranking and performance measurement. Augmenting content requires natural language processing (NLP) techniques like keyword and key phrase extraction, n-gram analysis, and word treatments including stemming and stop-word filtering. Ranking and retrieval of the right responses to queries use machine learning algorithms to measure the similarity of target content units of retrieval and the query itself. Finally, measuring retrieval performance is key to optimizing the quality of the experience, as managing the quality of the consumer search engine experiences is an ongoing task.

Despite the sophistication of consumer search engine development and the promises of AI and expert systems, designing an enterprise custom search experience that delivers against users’ high expectations can be challenging. Few guidelines exist to provide developers with a comprehensive view of processes and best practices to design, optimize, and improve custom search. Moreover, there are few tools that aid developers in the process of measuring how well their custom search engine performs at retrieving what the user intended to retrieve. From text pre-processing and enrichment to interactive querying and testing, each step could benefit from a process road map, how-to guidelines, and better tools. Enterprises have questions such as: Which techniques should be used at what time? What is the performance impact of different optimization choices on retrieval quality? Which set of optimizations performs the best?

In this project, we addressed the challenge of creating a custom domain experience. We leveraged Azure Search and Cognitive Services and we share our custom code for iterative testing, measurement and indexer redeployment. In our solution, the customized search engine will form the foundation for delivering a question and answer experience in a specific domain area. Below, we give you guidelines on designing your own custom search experience, followed by a step-by-step description of our work on this particular project with code and data that you can use to learn from and modify our approach for your in projects. In future posts, we’ll discuss the presentation layer as well as the work of integrating a custom Azure Search experience and Cognitive Services into a bot presentation experience.

## Designing a Custom Search Experience
Before we describe the solution for our project, we outline search design considerations. These design considerations will help you create an enterprise search experience that rivals the best consumer search engines.
The first step is to understand the custom search lifecycle, which involves designing the search experience, collecting and processing content, preparing the content for serving, serving and monitoring, and finally collecting feedback. Designing in continuous measurement and improvement is essential to developing and optimizing your search experience.

### Determine Your Target User and Intent
Defining youget user allows you to characterize the experience that they need and the query language that they will use. For example, if your target ur tarser is a domain expert, their query terminology reflects this expertise. On the other hand, if your target user is not familiar with the domain area covered, their queries won't include expert vocabulary.

Characterizing the intents of your target users guide your experience design and content strategy. In Web search engines, for instance, the user intent falls into one of three categories:
⦁	Navigational: Surfing directly to a specific website (e.g., MSN, Amazon or Wikipedia) 
⦁	Transactional: Completing a specific task (e.g., find a restaurant, reserve a table, sign up for a service) 
⦁	Informational: Browsing for general information about a topic using free-form queries (e.g., who is the director of Inception, artificial intelligence papers, upcoming events in Seattle)

Beyond these three categories, user intent may be further categorized into more specific sub-intents, especially for transactional and informational queries. Clarifying your user intents is foundational to serving the most relevant content in the clearest form. If possible, obtain a set of potential queries and characterize them by user intent.

### Consider the End-to-End Design
A good custom search design encompasses the end-to-end experience. Answering these ten key questions will give you a high-level set of requirements for your end-to-end custom search design.
1.	Which user intents or sub-intents will be supported?
2.	Is the content available to answer the user queries? Is there any data acquisition or collection that is required to assemble the necessary pieces of content?
3.	What type of content will be served: text, voice, multimedia or other?
4.	How will the content be served for each intent or sub-intent? How will the user interface work?
5.	Which delivery interface(s) will be supported (e.g., web page, mobile web page, chatbot, text, speech or other)?
6.	Will the experience include content from more than one source?
7.	Which user signals will be automatically captured for analysis? How?
8.	What type of user feedback will be solicited? How will it be solicited: implicitly or explicitly or both?
9.	What are the success metrics? Are they objective, subjective or both? How will they be computed?
10.	How do you compare alternative experiences? Will you run A/B testing or other testing protocol? How will you decide which experience is better in the potential situation of conflicting metrics?

### Characterize the Query and Consumption Interface and Experience
Once you have planned for the end-to-end experience, outline the content servicing and consumption experience. As you consider the query and results serving page layout, consider how many results you will need to deliver. The number of results you can serve is often a function of the screen size of the device where you are serving the experience, the character of the answers you are delivering, and the requirements of your target audience. It's key to think through delivering them in a consistent, visually and cognitively appealing layout.

### Define Success Measures and Feedback
Define your desired objective success metrics. Is success displaying the best answer in the top five responses, the top three responses, or just in the top one response? The success measures will be used in the optimization of the search experience, as well as for ongoing management. Consider measures you will need to optimize for launch and for ongoing performance management. Consider your approach to experimentation. Will you support A/B testing and flighting experiences to test different ranking mechanisms or user experiences?

Define how users will provide feedback on the quality of the answers or the quality of the experience. You may rely on implicit feedback from usage logs, for example, or explicit feedback the user provides based on the results served. Your UI affordances for explicit feedback might allow users to rate the usefulness of the specific result served, identify which result is the best, and rate the quality of the overall experience.

## Our Project Solution
A variety of services, tools, and platforms are available to assist in the content preparation and results serving, as well as in the online response to the incoming user queries. We reviewed the following services to identify which would serve the custom search experience requirements for our project.

⦁	Detection of user query intent/sub-intent via Language Understanding Intelligent Service (LUIS) 

⦁	Serving frequently asked questions via QnA Maker API 

⦁	Indexing and serving general search content via Azure Search 

⦁	Text analytics supporting tools, such as language detection, key phrase extraction, topic detection, sentiment analysis via Text Analytics API 

⦁	Other APIs supporting language, knowledge, speech, vision and more via	Microsoft Cognitive Services

Based on our content and target user requirements we identified Azure Search and the Language Understanding Intelligent Service as services we would use in our design.  

