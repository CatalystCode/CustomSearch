from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
import numpy as np
import codecs
import joblib

ans1 = codecs.open('EY_answers.txt', 'r', 'utf8').readlines()[1:]
ans2 = codecs.open('MS_answers.txt', 'r', 'utf8').readlines()[1:]
txt1 = [x.split('\t')[1] for x in ans1]
txt2 = [x.split('\t')[1] for x in ans2]

# Extend stopwords list to remove irrelevant domain words
stoplist = stopwords.words('english')
stoplist.extend(['section', 'subsection', 'sections', 'subsections', 'chapter', 'chapters', 'example', 'paragraph', 'paragraphs', 'regard', 'clause', 'subclause', 'case', 'subparagraph', 'subparagraphs','i', 'ii', 'iii', 'iv''v', 'vi', 'vii', 'viii', 'ix', 'x'])

#vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', encoding='utf-8')
vectorizer = TfidfVectorizer(ngram_range=(1,3), stop_words=list(stoplist), encoding='utf-8', lowercase=True)
tfidf2 = vectorizer.fit_transform(txt2)
tfidf1 = vectorizer.transform(txt1)

# Compute cosine similarities of one test vector
# cosine_sims = linear_kernel(tfidf[0:1], tfidf).flatten()
# np.argmax(cosine_sims)

# Compute all cosine similarity vectors for second set of anwers
cosine_sims = linear_kernel(tfidf2, tfidf1)
inds = cosine_sims.argmax(axis=1).squeeze()
sims = cosine_sims[np.arange(len(cosine_sims)) , inds]

# Write all similarities
outf = codecs.open('answers_sims.txt', 'w', 'utf8')
print >>outf, 'MS_AnsID\tEY_ID\tEY_AnsID\tSimilarity\tMS_Answer\tEY_Answer'
for i, ans in enumerate(ans2):
    msid, msans = ans.split('\t')
    if sims[i] == 0.0:
        print >>outf, '%s\t%d\t%s\t%f\t%s\t%s' % (msid, inds[i], -1, sims[i], msans.strip(), 'No match')
    else:
        eyid, eyans = ans1[inds[i]].split('\t')
        print >>outf, '%s\t%d\t%s\t%f\t%s\t%s' % (msid, inds[i], eyid, sims[i], msans.strip(), eyans.strip())
outf.close()

# Save TFIDF model
joblib.dump(vectorizer, 'ms_answers_tfidf.pkl')


