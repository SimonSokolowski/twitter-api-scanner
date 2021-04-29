from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import json

import twitter_credentials
 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.api = API(self.auth)
        self.numOfTweetsToFind = 100

    def stream_tweets(self, hash_tag_list):
        data = []
        for tweet in Cursor(self.api.search, q=hash_tag_list+" -filter:retweets", \
            lang="en", tweet_mode="extended").items(self.numOfTweetsToFind):
            tweets = tweet.full_text.replace("\n"," ")
            print(tweets)
            data.append({
                "tweet": tweets + "\n"
                })
        with open("data.txt", "w") as outfile:
            json.dump(data, outfile)

    # def on_data(self, data):
    #     try:
    #         #print(data)
    #         with open(self.fetched_tweets_filename, 'a') as tf:
    #             tf.write(data)
    #         return True
    #     except BaseException as e:
    #         print("Error on_data %s" % str(e))
    #     return True

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.API_Key, twitter_credentials.API_Key_Secret)
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)
        return auth

if __name__ == '__main__':
    hash_tag_list = ("apple stock OR #AAPL OR aapl")
    TwitterStreamer().stream_tweets(hash_tag_list)