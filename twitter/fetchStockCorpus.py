import os
from time import sleep
from twitter.twit_interface import TwitterInterface

TWEET_DIR = './tweet_corpus/'

if __name__ == '__main__':
    tickers = {
        'MMM': ['MMM', '3M'],
        'AXP': ['AmericanExpress', 'AMEX'],
        'AAPL': ['Apple'],
        'BA': ['Boeing'],
        'CAT': ['Caterpillar', 'CaterpillarInc'],
        'CVX': ['Chevron'],
        'CSCO': ['Cisco'],
        'KO': ['Coke', 'CocaCola'],
        'DOW': ['DowChemical', 'DowDupont'],
        'XOM': ['Exxon', 'ExxonMobil'],
        'GS': ['GoldmanSachs', 'Goldman'],
        'HD': ['HomeDepot', 'TheHomeDepot'],
        'IBM': ['IBM'],
        'INTC': ['Intel', 'IntelInside'],
        'JNJ': ['JandJ', 'Johnsonandjohnson'],
        'JPM': ['JPM', 'JPMorgan', 'JPMorganChase'],
        'MCD': ['McDonalds'],
        'MRK': ['Merck'],
        'MSFT': ['Microsoft'],
        'NKE': ['Nike'],
        'PFE': ['Pfizer'],
        'PG': ['ProcterandGamble', 'pandg'],
        'TRV': ['TravelersCompanies'],
        'UNH': ['UnitedHealth', 'UnitedHealthGroup'],
        'UTX': ['UnitedTech', 'UnitedTechnologies'],
        'VZ': ['Verizon'],
        'V': ['Visa'],
        'WMT': ['Walmart'],
        'WBA': ['Walgreens', 'WalgreensBoots'],
        'DIS': ['Disney', 'WaltDisney'],
        'random': ['placeholder']
    }

    tint = TwitterInterface()
    if not os.path.exists(TWEET_DIR):
        os.mkdir(TWEET_DIR)
    for ticker, hashtags in tickers.items():
        print(ticker)
        total = 0
        ticker_dir = TWEET_DIR + ticker + '/'
        if not os.path.exists(ticker_dir):
            os.mkdir(ticker_dir)
        for hashtag in hashtags:
            print(hashtag)
            attempts = 0
            tweets = ['placeholder']
            minid = None
            while len(tweets) > 0 and total < 10000:
                print(attempts)
                print(total)
                if ticker != 'random':
                    tweets = tint.get_tweets_for_hashtag(hashtag, minid)['statuses']
                else:
                    tweets = tint.get_random_tweets()['statuses']
                total += len(tweets)
                attempts += 1
                for tweet in tweets:
                    minid = min(minid if minid else 99999999999999999999, int(tweet['id']) - 1)
                    with open(ticker_dir + tweet['id_str'] + '.dat', 'w') as tweet_file:
                        print(tweet['full_text'], file=tweet_file)
                sleep(15)
