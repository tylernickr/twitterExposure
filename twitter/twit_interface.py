import json
from requests import sessions
from base64 import b64encode

ROOT_API = 'https://api.twitter.com/1.1'

cKey = 'OC8Ftw9EcOxWLTEUTT14rZx3J'
cSecret = 'Y5DwlJyuAP2KrfCXCKBxm0iuKOPgvK40fZWXvBb9NosfPwGAGZ'


class TwitterInterface(object):

    def __init__(self):
        self.s = sessions.session()
        full_key = cKey + ':' + cSecret
        encoded_bytes = b64encode(full_key.encode("utf-8"))
        final_key = str(encoded_bytes, "utf-8")

        auth_headers = {
            'Authorization': 'Basic ' + final_key,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        auth_params = {
            'grant_type': 'client_credentials'
        }
        resp = self.s.post('https://api.twitter.com/oauth2/token', headers=auth_headers, data=auth_params)
        auth_response = json.loads(resp.content)
        self.token = auth_response['access_token']

    def headers(self):
        return {
            'Authorization': 'Bearer ' + self.token
        }

    def get_user_profile(self, screen_name):
        params = {
            'screen_name': screen_name
        }
        resp = json.loads(self.s.get(ROOT_API + '/users/lookup.json', params=params, headers=self.headers()).content)
        return resp

    def get_random_tweets(self):
        params = {
            'q': 'the',
            'count': 100,
            'tweet_mode': 'extended',
            'lang': 'en',
            'result_type': 'recent'
        }
        resp = json.loads(self.s.get(ROOT_API + '/search/tweets.json', params=params, headers=self.headers()).content)
        return resp

    def get_tweets_for_hashtag(self, hashtag, max_id):
        params = {
            'q': '%23' + hashtag.lower(),
            'count': 100,
            'tweet_mode': 'extended',
            'max_id': max_id,
            'lang': 'en'
        }
        resp = json.loads(self.s.get(ROOT_API + '/search/tweets.json', params=params, headers=self.headers()).content)
        return resp

    def get_user_tweets(self, screen_name, max_id):
        params = {
            'screen_name': screen_name,
            'include_rts': False,
            'max_id': max_id,
            'count': 200
        }
        try:
            tweets = json.loads(self.s.get(ROOT_API + '/statuses/user_timeline.json',
                                       params = params,
                                       headers = self.headers()).content)
        except:
            return []
        return tweets

if __name__ == '__main__':
    twit = TwitterInterface()
    tweets = twit.get_random_tweets()
    print(tweets)