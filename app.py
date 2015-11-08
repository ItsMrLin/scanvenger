import os
from flask import Flask, request, send_from_directory, url_for, render_template
import model, helper

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/discover')
def discover():
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')

	data = {}
	if (latitude is not None and longitude is not None):
		latitude = float(latitude)
		longitude = float(longitude)
		data = {
			'latitude': latitude,
			'longitude': longitude
		}
		score_json = model.get_score(latitude, longitude)
		data['score_json'] = score_json

	return render_template('discover.html', data=data)


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