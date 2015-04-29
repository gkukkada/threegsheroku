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

		# This function is need to find out given hastag in particular locatio
		# If then make inside the geo location
		if 'entities' in decoded:
			i = 0
			num = len(decoded['entities']['hashtags'])
			bag = []
			while i < num:
				bag.append(decoded['entities']['hashtags'][i]['text'])
				i += 1
			hashtag = StreamListener.hashtag.replace('#', '')
			
			if hashtag in bag:
		
				# listen only for tweets that is geo-location enabled
				if 'geo' in decoded:
					
					tweet = {}
					tweet['screen_name'] = '@'+decoded['user']['screen_name']
					tweet['text'] = decoded['text'].encode('ascii', 'ignore')
					tweet['created_at'] = decoded['created_at']

					if decoded['geo']:
						StreamListener.tweetCounter = StreamListener.tweetCounter + 1
						if StreamListener.tweetCounter < StreamListener.stopAt:
							tweet['coord'] = decoded['geo']['coordinates']
							# publish to 'tweet_stream' channel
							redis.publish(tweet_stream, json.dumps(tweet))
							return True
						else:
							return False

						# Test with bounding 
					elif 'place' in decoded:
						if decoded['place']:
							pprint(decoded)
							#pprint(decoded['place']['bounding_box']['coordinates'])
							obj = decoded['place']['bounding_box']['coordinates'][0]
						
							lat1 = obj[0][0]
							lat2 = obj[1][0]
							lat3 = obj[2][0]
							lat4 = obj[3][0]

							lon1 = obj[0][1]
							lon2 = obj[1][1]
							lon3 = obj[2][1]
							lon4 = obj[3][1]

							lat = (lat1 + lat2 + lat3 + lat4) / 4
							lon = (lon1 + lon2 + lon3 + lon4) / 4
							pprint(lat)
							pprint(lon)
							tweet['coord'] = {lat, lon}
							redis.publish(tweet_stream, json.dumps(tweet))
					else:
						pass

	
	def on_error(self, status):
		print(status)

	def on_timeout(self):
		# this time is not worked
		print("Timeout...")
		time.sleep(10)
		return
