import tweepy

# Authentication

keys = open('keys', 'r').read().splitlines()
api_key = keys[1].split()[1]
api_key_secret = keys[2].split()[1]
access_token = keys[3].split()[1]
access_token_secret = keys[4].split()[1]

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Actions

tweet='This is an automated test tweet'
api.update_status(tweet)
