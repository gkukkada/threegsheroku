# Python
import os 
from pprint import pprint

# Flask
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/", methods=['GET', 'POST'])
def index():
	if 'hashtag' in session:
		session.pop('hashtag', None)

	if request.method == 'POST':
		""" get the form data using request form"""
		session['hashtag'] = request.form['hashtag']
		return redirect(url_for('map_view'))
	return render_template('handle/home.html')

@app.route('/map/')
def map_view():
	if 'hashtag' in session:
		return render_template('handle/map.html')
	else:
		return redirect(url_for('index'))

import tweepy
consumer_key = 'DZxeCAbMFENbXFR8wsYnx0jDv'
consumer_secret = 'Ph6CfSK63hXwR83QqUhxG53olOkf1p0o4CuzYOitgx49NisDc8'
access_token = '82060181-l7n0gUqTkaNpwVfneN27OCsYfvD8pzzzvLp1QKhEH'
access_token_secret = 'pfjUFZ7UNApyw3th9ANreI68uDJ9J0s7M9nt7oJgbaalk'

@app.route('/test/')
def test_view():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	stream = []
	for tweet in tweepy.Cursor(api.search, q='trending').items(10):
		print tweet.geo
		stream.append(tweet)
	return render_template('test.html', search=stream)

if __name__ == '__main__':
	app.run(debug=True)