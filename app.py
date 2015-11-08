import requests
import os
from flask import Flask, request, send_from_directory, url_for, render_template
from settings import APP_STATIC

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/discover')
def discover():
	# return requests.get('http://api.v3.factual.com/t/places-us?KEY=fJ1pTwv6Pbk8TamZ5T6wBoz1eeZT9dWagezor5sM&filters={"category_ids":{"$includes_any":[171, 445]}}&geo={"$circle":{"$center":[33.77, -84.39],"$meters":2000}}').content
    return render_template('discover.html')

@app.route('/saving')
def saving():
    return render_template('saving.html')

@app.route('/static/<path:path>')
def get_static(path):
	with open(os.path.join(APP_STATIC, path)) as f:
		return f.read()

@app.route('/api/get_score')
def get_score(path):
	return "{}"


if __name__ == '__main__':
    app.run(debug=True)