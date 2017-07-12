##############################
# Keyphrase extractor example
##############################

import os, sys
import pke
from nltk.corpus import stopwords

if len(sys.argv) < 2:
    print 'Missing content file name'
    print 'Usage %s filename [algo]' % os.path.basename(sys.argv[0])
    exit(1)

infile = sys.argv[1]
if len(sys.argv) >= 3:
    algo = sys.argv[2]
else:
    algo = 'topic'


def get_keyphrases(infile, mode='topic', postags=None, stoplist=None):
    if stoplist == None:
        stoplist = stopwords.words('english')
    if postags == None:
        postags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBN', 'VBD']

    # Run keyphrase extractor - TfIdf unsupervised method
    if mode == 'tfidf':
        extractor= pke.TfIdf(input_file=infile, language='english')
        extractor.read_document(format='raw', stemmer=None)
        extractor.candidate_selection(stoplist=stoplist)
        extractor.candidate_weighting()

    elif mode == 'topic':
        extractor = pke.TopicRank(input_file=infile, language='english')
        extractor.read_document(format='raw', stemmer=None)
        extractor.candidate_selection(stoplist=stoplist, pos=postags)
        #print extractor.candidates.keys()
        # Threshold = 1.0 keeps all candidates within clusters (i.e., compute weight only, no filter)
        #Lower tresholds filter candidates in topic_clustering - Default threshold = 0.25
        # Method: single, average, median, complete, centroid, ward, weighted
        extractor.candidate_weighting(threshold=0.25, method='average')
        #print extractor.candidates.keys()
        #print extractor.weights

    elif mode == 'single':
        extractor = pke.SingleRank(input_file=infile, language='english')
        extractor.read_document(format='raw', stemmer=None)
        extractor.candidate_selection(stoplist=stoplist)
        extractor.candidate_weighting(normalized=True)

    elif mode == 'kpminer':
        extractor = pke.KPMiner(input_file=infile, language='english')
        extractor.read_document(format='raw', stemmer=None)
        extractor.candidate_selection(stoplist=stoplist)
        extractor.candidate_weighting()

    else:   # invalid mode
        print "Invalid keyphrase extraction algorithm: %s" % mode
        print "Valid algorithms: [topic, single, kpminer, tfidf]"
        exit(1)

    phrases = extractor.get_n_best(500, redundancy_removal=True)
    return phrases


stoplist.extend(['section', 'subsection', 'sections', 'subsections', 'chapter', 'chapters', 'example', 'paragraph', 'paragraphs', 'regard', 'clause', 'subclause', 'case', 'subparagraph', 'subparagraphs','i', 'ii', 'iii', 'iv''v', 'vi', 'vii', 'viii', 'ix', 'x'])

# Select POS tags to use for candidate selection
#infile = './taxcode_dump/cleancontent/1.1.1.1.1.1.splitdump.txt'
#infile = './taxcode_dump/cleancontent/1.1.1.1.4.3.6_content.txt'

postags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBN', 'VBD']
#postags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBN', 'VBD', 'VBG']

##############################
# Main processing
##############################

# Extend stopwords list to remove irrelevant domain words
stoplist = stopwords.words('english')
phrases = get_keyphrases(infile, mode=algo, postags=postags, stoplist=stoplist)
print 'Number of extracted keyphrases = %d' % len(phrases)
for phrase in phrases:
    print phrase

#out = ' '.join(p[0] for p in phrases)
#print out.encode('utf8')
