# CustomDomainSearch
Custom Search Experience 



The need
to navigate specific content areas via question and answers is a common
scenario across enterprises.  Enabling fast traversal of specialized
publications, customer support knowledge bases or document repositories are
common needs.  Simple FAQ’s don’t cover enough ground, and keyword search
isn’t effective or efficient for those not familiar with the domain or the
document set.  Instead, enterprises can deliver a custom search
experiences that save their clients time and provide better service. And users
have very high expectations for search engine efficiency and quality.

Consumer
search engines combine many sophisticated techniques to provide the best
results.  From augmenting and indexing
target content to augmenting search queries, to retrieval ranking and
performance measurement, consumer search engines employ several processes to
deliver the best results.   Indexing and
augmenting content involves natural language processing (NLP) techniques
including approaches like keyword and key phrase extraction, n-gram analysis, and
word treatments like stemming and stop-word filtering. Ranking and retrieval of
the right responses to queries leverages machine learning algorithms to measure
similarity of target content units of retrieval and the query itself.  Finally, measuring retrieval performance is
key to optimizing the quality of the experience, and managing consumer search
engine experiences ongoing.

Despite
the promise of AI and expert systems, designing a custom search experience for
enterprise that delivers against users’ high expectations can be challenging.
Few guidelines exist to provide developers with a comprehensive view of
processes and best practices to design, optimize, and improve custom search.  Moreover, there are few tools that aid
developers in the process of measuring how well their custom search engine
performs at retrieving what the user intended to retrieve.  From text
pre-processing and enrichment to interactive querying and testing, each step
could benefit from a process road map, how-to guidelines and better tools.
Enterprises have questions including; Which techniques should be used at what
time? What is the performance impact of different optimization choices on
retrieval quality? Which set of optimizations perform the best?

We
worked with one of the global ‘Big Four’ professional services firms
to help them develop and improve performance on a custom search engine to power
a self-service expert system leveraging category-specific advisory
publications.  The users of their expert system require an
efficient and reliable experience, with a high degree of accuracy in the set of
answers provided.  We share our
learnings, process and custom code here.

In
this project, we describe how we addressed the challenge of creating
a custom domain search question and answer experience, leveraging Azure
Search and Cognitive Services and custom code for iterative testing, measurement
and indexer redeployment.  In the solution, we
describe primarily designing and optimizing a customizing search
engine for a specific domain area.  This customized search engine
is the foundation for delivering the question and answer
experience.  In other posts, we’ll discuss the presentation
layer, including the bot framework, in more depth, and the work of integrating
a custom Azure Search experience and Cognitive Services into a bot presentation
experience.

