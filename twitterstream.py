#!venv/bin/python

# all the imports
from flask import Flask, request
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

import os
import redis

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)

import tweepy
import json

from pprint import pprint
import time

red = redis.StrictRedis()


# listener that handles streaming data
class StreamListener(tweepy.StreamListener):
	tweetCounter = 0
	stopAt = 100
	
	def on_connect(self):
		print( "Stream Starting...")

	def on_status(self, status):
		# We can't get status here... No reason
		return

	# method called when raw data is received from connection
	def on_data(self, data):
		tweet_stream =  StreamListener.userid
		decoded = json.loads(data)
		# listen only for tweets that is geo-location enabled
		if 'geo' in decoded:
			if decoded['geo']:
				StreamListener.tweetCounter = StreamListener.tweetCounter + 1
				print(StreamListener.tweetCounter)
				if StreamListener.tweetCounter < StreamListener.stopAt:
					tweet = {}
					tweet['screen_name'] = '@'+decoded['user']['screen_name']
					tweet['text'] = decoded['text'].encode('ascii', 'ignore')
					tweet['coord'] = decoded['geo']['coordinates']
					tweet['created_at'] = decoded['created_at']
					print( 'A tweet received')
					# publish to 'tweet_stream' channel
					red.publish(tweet_stream, json.dumps(tweet))
					return True
				else:
					return False
	
	def on_error(self, status):
		print(status)

	def on_timeout(self):
		print("Timeout...")
		time.sleep(10)
		return