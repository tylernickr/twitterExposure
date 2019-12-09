import os
from re import match, sub
from nltk import word_tokenize
from enchant import Dict
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
for word in ['rt', 'co', 'amp']:
    stopwords.add(word)
word_dict = Dict("en_US")
stemmer = PorterStemmer()

TOKEN_DIR = './tokenized_corpus/'
RAW_TWEET_DIR = './tweet_corpus/'

if __name__ == '__main__':
    if not os.path.exists(TOKEN_DIR):
        os.mkdir(TOKEN_DIR)
    for ticker in os.listdir(RAW_TWEET_DIR):
        tickerpath = RAW_TWEET_DIR + ticker + '/'
        ticker_token_file = TOKEN_DIR + ticker + '.dat'
        with open(ticker_token_file, 'w') as token_file:
            for filename in os.listdir(tickerpath):
                tweet_id = match("(.*)\.dat", filename).group(1)
                content = open(tickerpath + filename).read()
                content = content.lower()
                content = sub('\W+', ' ', content)
                tokens = word_tokenize(content)
                tokens = [stemmer.stem(x) for x in tokens if x not in stopwords
                          and len(x) > 1
                          and word_dict.check(x)]
                print(','.join(tokens), file=token_file)

