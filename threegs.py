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

if __name__ == '__main__':
	app.run(debug=True)