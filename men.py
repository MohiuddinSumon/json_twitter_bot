from pprint import pprint

from config import create_client, o2_client

# client = o2_client()
client = create_client()
# response = client.get_me()
# me = response.data
# print(me, me.id, dir(me))
# print(client.get_users_mentions(me.id))
# jsn = client.get_user(username='jsnNFT')
jsn = client.get_user(username='MohiuddinASumon')
print(jsn)

# <User id=1455312084758155272 name=jsnNFT username=jsnNFT>

parent_tweet = '1509481447786102789'
# client.like(parent_tweet)
# client.create_tweet(in_reply_to_tweet_id=parent_tweet, text='Hello @0xafters @SnipeNFTs @prasdiman')


# 1509431278663348226
tweet = client.get_tweet(id=1511004185096974336, expansions="author_id,in_reply_to_user_id", 
        tweet_fields='conversation_id')

print(tweet,dir(tweet))
print(tweet.data, tweet.includes)

for k,v in tweet.data.items():
    print(f'\tFor {k} = {v} \n')

# 1032825366543360001
