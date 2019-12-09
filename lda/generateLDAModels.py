import os
from re import match
from scipy.sparse import coo_matrix
from sklearn.decomposition import LatentDirichletAllocation
from joblib import dump

TOKEN_FILE_DIR = '../twitter/tokenized_corpus/'
LDA_DIR = './data/'

if __name__ == '__main__':
    if not os.path.exists(LDA_DIR):
        os.mkdir(LDA_DIR)
    completed = os.listdir(LDA_DIR)
    for ticker_filename in [x for x in os.listdir(TOKEN_FILE_DIR) if x != 'random.dat']:
        ticker = match('(.*)\.dat', ticker_filename).group(1)
        if ticker not in completed:
            ticker_dir = LDA_DIR + ticker + '/'
            if not os.path.exists(ticker_dir):
                os.mkdir(ticker_dir)
            word_idx_map = {}
            current_idx = 0
            rec_count = 0
            tick_rec_count = 0
            for filename in [ticker_filename, 'random.dat']:
                for line in open(TOKEN_FILE_DIR + filename):
                    rec_count += 1
                    if filename == ticker_filename:
                        tick_rec_count += 1
                    else:
                        if rec_count == tick_rec_count * 2:
                            break
                    line = line[:-1]
                    tokens = line.split(',')
                    for token in tokens:
                        try:
                            word_idx_map[token]
                        except KeyError:
                            word_idx_map[token] = current_idx
                            current_idx += 1

            records = []
            columns = []
            rec_count = 0
            for filename in [ticker_filename, 'random.dat']:
                for line in open(TOKEN_FILE_DIR + filename):
                    rec_count += 1
                    if rec_count == tick_rec_count * 2:
                        break
                    line = line[:-1]
                    tokens = line.split(',')
                    data = []
                    i = []
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
            wc_vector = coo_matrix((data, (i, j)))
            lda = LatentDirichletAllocation(n_components=100)
            lda.fit(wc_vector)
            print(ticker)
            print(len(records))
            with open(ticker_dir + 'wordidx.dat', 'w') as wordidx_file:
                for word, idxloc in word_idx_map.items():
                    print(','.join([word, str(idxloc)]), file=wordidx_file)
            dump(lda, ticker_dir + ticker + '.pickle')

