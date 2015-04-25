#authors: threegs(threegsksu@gmail.com)

#!venv/bin/python

# all the imports
from flask import Flask, request
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

import tweepy
from store import redis
import json

from pprint import pprint
import time

#red = redis.StrictRedis()


# listener that handles streaming data
class StreamListener(tweepy.StreamListener):
	tweetCounter = 0
	stopAt = 200
	
	def on_connect(self):
		print( "Stream Starting...")

	def on_status(self, status):
		# We can't get status here... No reason
		return

	# method called when raw data is received from connection
	def on_data(self, data):
		tweet_stream =  StreamListener.userid
		redis.client_setname(tweet_stream)
		decoded = json.loads(data)
		# listen only for tweets that is geo-location enabled
		if 'geo' in decoded:
			if decoded['geo']:
				StreamListener.tweetCounter = StreamListener.tweetCounter + 1
				if StreamListener.tweetCounter < StreamListener.stopAt:
					tweet = {}
					tweet['screen_name'] = '@'+decoded['user']['screen_name']
					tweet['text'] = decoded['text'].encode('ascii', 'ignore')
					tweet['coord'] = decoded['geo']['coordinates']
					tweet['created_at'] = decoded['created_at']
					# publish to 'tweet_stream' channel
					redis.publish(tweet_stream, json.dumps(tweet))
					return True
				else:
					return False
	
	def on_error(self, status):
		print(status)

	def on_timeout(self):
		# this time is not worked
		print("Timeout...")
		time.sleep(10)
		return
