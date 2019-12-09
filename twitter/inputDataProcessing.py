import os
from re import match, sub
from nltk import word_tokenize
from enchant import Dict
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from scipy.sparse import coo_matrix
from datetime import datetime
from joblib import load
stopwords = set(stopwords.words('english'))
for word in ['rt', 'co', 'amp']:
    stopwords.add(word)
word_dict = Dict("en_US")
stemmer = PorterStemmer()

RAW_TWEET_DIR = './tweet_data/'
LDA_MODEL_DIR = '../lda/data/'
PROCESSED_DIR = './processed_tweet_data/'


def get_coo_vector(word_idx_map, token_list):
    records = []
    columns = []
    rec_count = 0
    for tokens in token_list:
        rec_count += 1

        data = []
        j = []
        word_count = {}
        for token in tokens:
            try:
                word_count[token] += 1
            except KeyError:
                word_count[token] = 1
        for token in tokens:
            tok_idx = word_idx_map[token]
            data.append(word_count[token])
            j.append(tok_idx)
        columns.append(j)
        records.append(data)

    data = []
    i = []
    j = []
    for row in range(len(records)):
        data += records[row]
        j += columns[row]
        i += [row] * len(records[row])
    return coo_matrix((data, (i, j)))


def get_word_idx_map(filename):
    word_idx_map = {}
    for line in open(filename):
        word, idx = line[:-1].split(',')
        word_idx_map[word] = int(idx)
    return word_idx_map


if __name__ == '__main__':
    if not os.path.exists(PROCESSED_DIR):
        os.mkdir(PROCESSED_DIR)

    token_list = []
    for screen_name in os.listdir(RAW_TWEET_DIR):
        sn_dir = RAW_TWEET_DIR + screen_name + '/'
        for filename in os.listdir(sn_dir):
            with open(sn_dir + filename) as tfile:
                tdate = datetime.strftime(tfile.readline()[:-1])
                content = tfile.readline()[:-1]
                content = content.lower()
                content = sub('\W+', ' ', content)
                tokens = word_tokenize(content)
                tokens = [tdate] + [stemmer.stem(x) for x in tokens if x not in stopwords
                          and len(x) > 1
                          and word_dict.check(x)]
                token_list.append(tokens)
    for ticker in os.listdir(LDA_MODEL_DIR):
        word_idx_map = get_word_idx_map(LDA_MODEL_DIR + ticker + '/wordidx.dat')
        wc_matrix = get_coo_vector(word_idx_map, token_list)
        print(wc_matrix)