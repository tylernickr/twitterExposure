import os
from twitter.twit_interface import TwitterInterface
from time import sleep

TWEET_DIR = './tweet_data/'

screen_names = [
    'foxnews',
    'abcnewslive',
    'skynewsbreak',
    'cbstopnews',
    'reuterslive',
    'wsjbreakingnews',
    'cnnbrk',
    'barackobama',
    'realdonaldtrump',
    'jpmorgan',
    'goldmansachs',
    'federalreserve',
    'breakingnews',
    'cnbc',
    'benzinga',
    'stocktwits',
    'breakoutstocks',
    'bespokeinvest',
    'wsjmarkets',
    'nytimesbusiness',
    'ibdinvestors',
    'wsjdealjournal',
    'business',
    'livesquawk',
    'keithmccullough',
    'zerohedge',
    'foxbusiness',
    'thomsonreuters',
    'forbes',
    'harvardbiz'
]


if __name__ == '__main__':
    tint = TwitterInterface()
    if not os.path.exists(TWEET_DIR):
        os.mkdir(TWEET_DIR)
    for user in screen_names:
        print(user)
        minid = None
        user_dir = TWEET_DIR + user + '/'
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        tweets = ['placeholder']
        while len(tweets) > 0:
            len(tweets)
            sleep(5)
            tweets = tint.get_user_tweets(user, minid)
            print(tweets)
            for tweet in tweets:
                minid = min(minid if minid else 99999999999999, tweet['id'])
                with open(user_dir + tweet['id_str'] + '.dat', 'w') as tweet_file:
                    print(tweet['created_at'], file=tweet_file)
                    print(tweet['text'], file=tweet_file)