# Python
import os 
from pprint import pprint

# Flask
from flask import Flask, render_template, request, redirect, url_for, session, stream_with_context, Response

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

import tweepy
from twitterstream import StreamListener
from store import redis
#red = redis.StrictRedis()

from random import randint

# OAuth process
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

@app.route("/", methods=['GET', 'POST'])
def index_view():
	if request.method == 'POST':
		session['hashtag'] = request.form['hashtag']
		return redirect(url_for('map'))
	return render_template('handle/home.html')


@app.route("/map", methods=['GET', 'POST'])
def map():
	""" get the form data using request form"""
	hashtag = session['hashtag']
	#i = list(hashtag)
	if hashtag[0] == '#':
		track = hashtag
	else:
		track = ['#{}'.format(hashtag)]

	""" gonna starts here """
	session['random_userid'] = randint(1, 999)
	StreamListener.userid = session['random_userid']
	
	###########################################
	def handler(signum, frame):
		print("Forever is over")
		raise Exception("end of time")

	def main_stream():
		stream = tweepy.Stream(auth, StreamListener())
		stream.filter(track=track,async=True)
		redirect(url_for('map_stream'))

	def close_stream():
		""" get the client list and delete """
		obj = redis.client_list(tweet_stream)
		redis_client_list = obj[0]['addr']
		pprint(redis_client_list)
		redis.client_kill(redis_client_list)
		stream = tweepy.Stream(auth, StreamListener())
		stream.disconnect()

	import signal
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(300)
	try:
		main_stream()
	except Exception:
		close_stream()
		print("function terminate")

	return render_template('handle/map.html')

@app.route('/map-stream')
def map_stream():
	def event_stream():
		pubsub = redis.pubsub()
		pubsub.subscribe(session['random_userid'])
		for message in pubsub.listen():
			yield 'data: %s\n\n' % message['data']
	return Response(stream_with_context(event_stream()), mimetype="text/event-stream")

@app.route('/close-stream')
def close_stream():
	pprint(redis.quit)
	return "Finish"

@app.route('/test')
def test_view():
	session['close'] = "yesiamgonnadelete"
	return redirect(url_for('index_view'))
	

if __name__ == '__main__':
	app.run(debug=True)
