import requests
import helper
import json

base_api_link = 'http://api.v3.factual.com/t/places-us?KEY=fJ1pTwv6Pbk8TamZ5T6wBoz1eeZT9dWagezor5sM'
place_type = [171, 445]

census_data_path = 'data/census2010.csv'

def get_score(latitude, longitude):
	places = json.loads(helper.get_static("mock/local.json"))['response']['data']
	# places = get_neighbors(latitude, longitude)
	zip_to_population = helper.load_csv_as_dict(census_data_path)
	print zip_to_population
	return str(zip_to_population['10011'])
	# return 

def get_neighbors(latitude, longitude, radius=2000):
	attached = '&filters={"category_ids":{"$includes_any":' + str(place_type) + '}}&geo={"$circle":{"$center":[' + str(latitude) + ', ' + str(longitude) + '],"$meters":' + str(radius) + '}}'
	request_link = base_api_link + attached
	content = requests.get(request_link).content
	data = json.loads(content['response']['data'])
	return data
