import logging
import time
from xml.dom import UserDataHandler

import tweepy

from config import create_api, create_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id

    # for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
    for tweet in tweepy.Cursor(api.get_users_mentions('1032825366543360001'), since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        print(f' DFSF { tweet} ')
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="Please reach us via DM",
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    # api = create_api()
    client = create_client()
    since_id = 1
    # client.get_users_mentions()
    while True:
        # user_data = client.get_me()
        # print(user_data, dir(user_data))
        # user = user_data.data
        # print(user, user.id, user.username)

        json_data = client.get_user(username='1superfuture1')
        jsn = json_data.data
        print(jsn.id, jsn.username, jsn)
        mentions = client.get_users_mentions(jsn.id).data
        # print(f'Mentions are = {mentions}')
        for mention in mentions:
            print(f'Tweet ID = {mention.id} and TEXT = {mention.text}')

        # since_id = check_mentions(client, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
