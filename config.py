import logging
from multiprocessing.dummy import active_children

import tweepy
from decouple import config

API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')

USER_ACCESS_TOKEN = config('USER_ACCESS_TOKEN')
USER_ACCESS_TOKEN_SECRET = config('USER_ACCESS_TOKEN_SECRET')

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')

logger = logging.getLogger()

def create_api():

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key=API_KEY, consumer_secret=API_SECRET)
    auth.set_access_token(USER_ACCESS_TOKEN, USER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def create_client():
    return tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=USER_ACCESS_TOKEN,
        access_token_secret=USER_ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True,
    )


def o2_client():
    auth = tweepy.OAuth2UserHandler(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='https://mpmohi.com/',
        scope='tweet.read tweet.write'
    )

    print(auth.get_authorization_url())
    response_url = input("Provide response url ")
    access_token = auth.fetch_token(response_url)
    print(access_token)
    at = access_token['access_token']
    print(at)
    client = tweepy.Client(at)
    return client
