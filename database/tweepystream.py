import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import json
import sqlite3
from unidecode import unidecode
import time
import datetime

#import the API keys from the config file.
#from database.config import con_key, con_sec, a_token, a_secret
from config import con_key, con_sec, a_token, a_secret

#conn = sqlite3.connect(r"database\wine_data.sqlite")
conn = sqlite3.connect(r"wine_data.sqlite")
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS wineTweets(timestamp REAL, tweet TEXT)")
    conn.commit()

create_table()

class WineListener(StreamListener):
    def on_data(self, data):
            try:
                data = json.loads(data)
                tweet = unidecode(data['text'])
                time_ms = data['timestamp_ms']
                #print(tweet, time_ms) ############################################  TO PRINT OUT THE TWEETS IN THE CONSOLE
                c.execute("INSERT INTO wineTweets (timestamp, tweet) VALUES (?, ?)", (time_ms, tweet))

                conn.commit()
                time.sleep(2)
            
            except KeyError as e:
                print(str(e))
            
            return(True)

    def on_error(self, status_code):
        if status_code == 420:
                #returning False in on_error disconnects the stream
                return False
            
while True:
    try:
        auth = OAuthHandler(con_key, con_sec)
        auth.set_access_token(a_token, a_secret)
        twitterStream = tweepy.Stream(auth, WineListener())        
        twitterStream.filter(track=['wine']) #####################################

    except Exception as e:
        print(str(e))
        time.sleep(4)