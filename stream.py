import json
import os
from pydoc import cli

import requests
from decouple import config

from config import create_client

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = config("BEARER_TOKEN")
JSN_ID = config('JSN_ID')


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print("Rules response = ", json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print("Delete Response = ", json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "@1superfuture1", "tag": "Superfuture Mentioned"},
    ]
    payload = {
        "add": sample_rules
    }
    query_params = {
        "expansions": "author_id",
        "tweet.fields": "conversation_id",
    }
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
        params=query_params
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print("SET RULES = ", json.dumps(response.json()))


def get_stream(set, client):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet_id = json_response['data']['id']
            print(json.dumps(json_response, indent=4, sort_keys=True))
            print(tweet_id)
            tweet_object = client.get_tweet(id=tweet_id, expansions="author_id,in_reply_to_user_id", 
                                            tweet_fields='conversation_id')
            tweet = tweet_object.data
            print(tweet_object, tweet)
            parent_tweet = tweet.conversation_id
            parent_user_id = tweet.in_reply_to_user_id
            print(parent_tweet, parent_user_id)
            # 1510490915432849409
            client.like(parent_tweet)
            client.retweet(parent_tweet)
            client.create_tweet(in_reply_to_tweet_id=tweet_id, text='@0xafters @SnipeNFTs @prasdiman')
            tweet_author = tweet_object.includes
            print(tweet, tweet_author)



def main():
    client = create_client()
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set, client)


if __name__ == "__main__":
    main()
