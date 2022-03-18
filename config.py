import os

import tweepy
from decouple import config

API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')

USER_TOKEN = config('USER_TOKEN')
USER_SECRET = config('USER_SECRET')


# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key=API_KEY, consumer_secret=API_SECRET)
auth.set_access_token(USER_TOKEN, USER_SECRET)

api = tweepy.API(auth)

try:
    print("Authentication OK")
except Exception as e:
    print(f"Error during authentication {e}")


user = api.get_user(screen_name='twitter')
print(user)

# home = api.home_timeline()
# print(home)
