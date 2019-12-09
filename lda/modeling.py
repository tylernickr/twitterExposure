import os
import numpy as np
import pandas as pd
from re import match
from scipy.sparse import coo_matrix
from joblib import load
from sklearn.model_selection import cross_validate
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

MODELING_DIR = './modeling/'
LDA_DIR = './data/'
RAW_DATA_DIR = '../twitter/tokenized_corpus/'


def get_lda_model(ticker):
    lda = load(LDA_DIR + ticker + '/' + ticker + '.pickle')
    return lda


def get_word_idx_map(filename):
    word_idx_map = {}
    for line in open(filename):
        word, idx = line[:-1].split(',')
        word_idx_map[word] = int(idx)
    return word_idx_map


def get_dataframe(ticker):
    word_idx_map = get_word_idx_map(LDA_DIR + ticker + '/wordidx.dat')
    label_idx = max([x for x in word_idx_map.values()]) + 1

    records = []
    columns = []
    ticker_rows = 0
    rows = 0
    for filename in [ticker_filename, 'random.dat']:
        for line in open(RAW_DATA_DIR + filename):
            rows += 1
            if filename == ticker_filename:
                ticker_rows += 1
            else:
                if rows > ticker_rows * 2:
                    break
            line = line[:-1]
            tokens = line.split(',')
            data = []
            j = []
            word_count = {}
            for token in tokens:
                try:
                    word_count[token] += 1
                except KeyError:
                    word_count[token] = 1
            for token in tokens:
                try:
                    tok_idx = word_idx_map[token]
                    data.append(word_count[token])
                    j.append(tok_idx)
                except KeyError:
                    pass
            data.append(1 if filename != 'random.dat' else 0)
            j.append(label_idx)
            columns.append(j)
            records.append(data)

    data = []
    i = []
    j = []
    for row in range(len(records)):
        data += records[row]
        j += columns[row]
        i += [row] * len(records[row])
    wc_sparse_vector = coo_matrix((data, (i, j)))
    wc_data = pd.DataFrame(data=wc_sparse_vector.toarray())
    return wc_data


if __name__ == '__main__':
    if not os.path.exists(MODELING_DIR):
        os.mkdir(MODELING_DIR)

    for ticker_filename in [x for x in os.listdir(RAW_DATA_DIR) if x != 'random.dat']:
        ticker = match('(.*)\.dat', ticker_filename).group(1)
        raw_data = get_dataframe(ticker)
        raw_data = raw_data.sample(frac=1).reset_index(drop=True)
        raw_input = raw_data[raw_data.columns[:-1]].values
        labels = raw_data[raw_data.columns[-1]].values
        lda = get_lda_model(ticker)
        clean_data = lda.transform(raw_input)
        print(ticker)
        #mymodel = LogisticRegression(solver='lbfgs')
        #mymodel = AdaBoostClassifier()
        mymodel = RandomForestClassifier(n_estimators=100)
        results = cross_validate(mymodel,
                             clean_data,
                             labels,
                             cv=5)
        print(results['test_score'])
