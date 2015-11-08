import os
from flask import Flask, request, send_from_directory, url_for, render_template
import model, helper

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
	page = {
		'title':'sCANvenger',
		# 'nav_title': 'Welcome!',
		# 'prev_page': 'index.html'
	}
	return render_template('index.html', page=page)

@app.route('/discover')
def discover():
	page = {
		'title':'Discover',
		'nav_title': 'Discover',
		'prev_page': '/picker-home'
	}

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

	return render_template('discover.html', data=data, page=page)

@app.route('/center-home')
def center_home():
    return render_template('center-home.html')

@app.route('/nessie-demo')
def nessie_demo():
    return render_template('nessie-demo.html')

@app.route('/picker-home', methods=['GET', 'POST'])
def picker_home():
	data = {}
	if request.method == 'POST':
		data['id'] = request.form['id']
	return render_template('picker-home.html', data=data)

@app.route('/picker-login', methods=['GET', 'POST'])
def picker_login():
	if request.method == 'POST':
		return render_template('picker-login.html', is_post = True)
	else:
		return render_template('picker-login.html', is_post = False)

@app.route('/picker-signup', methods=['GET', 'POST'])
def picker_signup():
	if request.method == 'POST':
		return render_template('picker-signup.html', is_post = True)
	else:
		return render_template('picker-signup.html', is_post = False)


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