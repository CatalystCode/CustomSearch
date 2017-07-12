#
# Compute similarities and check overlap between answers
#
import difflib
import re, string
import sys
import codecs
import joblib
import numpy as np
import pandas as pd

INDIR       = './hackfest'
EY_QA_Pairs = INDIR + '/700-QA-pairs.xlsx'
#MS_ANS_BASE = '/MS-azanswers-mh-eytaxidxer-top5'
MS_ANS_BASE = '/Test-azanswers-mh-eytaxidxer-top5'
MS_Answers  = INDIR + MS_ANS_BASE + '.txt'
SIM_OUTPUT  = INDIR + MS_ANS_BASE + '_sims.txt'
SIM_EXCEL   = INDIR + MS_ANS_BASE + '_sims.xlsx'
TFIDF_MODEL = INDIR + '/ms_full_answers_tfidf_ngram=1-3.pkl'

# Compute difference between two sequences
# A quick way to get a similarity measure between two pieces of s
def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()

# Strip non-ascii characters that break the overlap check
def strip_non_ascii(s):
    s = (c for c in s if 0 < ord(c) < 127)
    s = ''.join(s)
    return s

# Compact strings then check if one string contains the other
# Clean string of all non-alphanumeric and remove spaces to maximize similarity
def clean(s):
    #s = re.sub('\W+','', s.lower())
    s = re.sub('[^a-z]','', s.lower())
    return s

# Check if string is contained in another
def isSubset(a, b):
    a   = clean(a)
    b   = clean(b)
    la  = float(len(a))
    lb  = float(len(b))
    seq = difflib.SequenceMatcher(None, a, b)
    # Find matching blocks to address cases of minor misalignment
    blocks = seq.get_matching_blocks()
    match  = 0
    for m in blocks:
        match += m.size
    # In case get_matching_blocks() does not find the longest match
    longest = seq.find_longest_match(0, len(a), 0, len(b))
    if match < longest.size:
        match = longest.size
    if a == b:
        return 'Exact match'
    #elif a in b or match == la:
    elif a in b or (match/la > 0.9):
        return 'EY in MS'
    #elif b in a or match == lb:
    elif b in a or (match/lb > 0.9):
        return 'MS in EY'
    elif len(blocks) == 2:   # get_matching_blocks() adds a dummp block
        return 'Overlapping'
    else:
        return 'No overlap'

# Compute TFIDF similarity
def cosinesim(vectorizer, s1, s2):
    tfidf1 = vectorizer.transform([s1])
    tfidf2 = vectorizer.transform([s2])
    #cosinesim = np.dot(tfidf1, tfidf2.T)[0,0]
    cosinesim = (tfidf1 * tfidf2.T)[0,0]
    return cosinesim


if __name__ == '__main__':
    #if len(sys.argv) < 3:
    #    print('Missing arguments. Usage: %s [file1] [file2]' % sys.argv[0])
    #    exit(1)

    #ey_df  = pd.read_csv(EY_QA_Pairs, sep='\t', quoting=3, encoding='utf-8')
    ey_df  = pd.read_excel(EY_QA_Pairs, quoting=3, encoding='utf-8')
    ms_df  = pd.read_csv(MS_Answers,  sep='\t', quoting=3, encoding='utf-8')
    ey_df['Qid'] = ey_df['Qid'].astype('int')
    ms_df['Qid'] = ms_df['Qid'].astype('int')

    # Output dataframe
    df = pd.DataFrame(columns = ['Qid', 'Question', 'EY_Answer', 'MS_Rank', 'MS_Answer', 'Overlap', 'Diff_Sim', 'Tfidf_Sim'], dtype=unicode)

    # Load TFIDF model
    vectorizer = joblib.load(TFIDF_MODEL)
    for eid, row in ey_df.iterrows():
        qid      = row['Qid']
        question = row['Question']
        ey_ans   = row['Answer']
        print 'Processing answers for question# %s' % qid

        docs = ms_df[ms_df['Qid'] == qid]
        #print len(docs)
        for mid, doc in docs.iterrows():
            ms_ans  = doc['Answer']
            rank    = doc['Rank']

            # Compute overlap and sting similarity
            overlap   = isSubset(ey_ans, ms_ans)
            diff_sim  = similar(ey_ans, ms_ans)
            tfidf_sim = cosinesim(vectorizer, ey_ans, ms_ans)
            # If high similarity but overlap was not detected by isSubset
            if overlap == 'No overlap' and diff_sim > 0.5 and tfidf_sim > 0.5:
                overlap = 'High similarity'

            out_row = {'Qid'      : qid, 
                       'Question' : question,
                       'EY_Answer': ey_ans,
                       'MS_Rank'  : rank,
                       'MS_Answer': ms_ans,
                       'Overlap'  : overlap,
                       'Diff_Sim' : diff_sim,
                       'Tfidf_Sim': tfidf_sim}

            df = df.append(out_row, ignore_index=True)

    # Save similarities output
    df['Qid']     = df['Qid'].astype(int)
    df['MS_Rank'] = df['MS_Rank'].astype(int)
    df.to_csv(SIM_OUTPUT, sep='\t', index=False, encoding='utf-8')    
    df.to_excel(SIM_EXCEL, index=False, encoding='utf-8')    


