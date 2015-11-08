import os
from flask import Flask, request, send_from_directory, url_for, render_template
import model, helper

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/discover')
def discover():
    return render_template('discover.html')


@app.route('/saving')
def saving():
    return render_template('saving.html')

# @app.route('/api/get_score')
# def get_score():
# 	latitude = request.args.get('latitude')
# 	longitude = request.args.get('longitude')
# 	return helper.get_static("mock/local_score.json")

@app.route('/api/get_score')
def get_score():
	latitude = float(request.args.get('latitude'))
	longitude = float(request.args.get('longitude'))
	return model.get_score(latitude, longitude)


if __name__ == '__main__':
    app.run(debug=True)