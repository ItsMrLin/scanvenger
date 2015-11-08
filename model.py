import requests
import helper
import json
import numpy as np
from scipy.stats import norm
from math import radians, cos, sin, asin, sqrt


census_data_path = 'data/census2010.csv'
zip_to_population = helper.load_csv_as_dict(census_data_path)

BASE_API_LINK = 'http://api.v3.factual.com/t/places-us?KEY=fJ1pTwv6Pbk8TamZ5T6wBoz1eeZT9dWagezor5sM'
PLACE_TYPE = [171, 445]

DRINKS_SOLD_PER_STORE_PER_DAY = 650
SINGLE_DRINK_PRICE = 40.0 / 700.0
DAILY_ACTIVE_HOUR = 8.0

DEFAULT_RADIUS = 1000

def _haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    # print type(lon1), type(lat1), type(lon2), type(lat2)
    # print lon1, lat1, lon2, lat2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def get_score(latitude, longitude, size_n = 10, influence_range_in_meter = 1000):
	# places_raw = json.loads(helper.get_static("mock/local.json"))['response']['data']
	get_neighbor_radius = DEFAULT_RADIUS
	places_raw = get_neighbors(latitude, longitude, get_neighbor_radius)


	while (len(places_raw) == 0):
		get_neighbor_radius *= 2
		places_raw = get_neighbors(latitude, longitude, get_neighbor_radius) 

	places = []
	minLat = 9999
	minLong = 9999
	maxLat = -9999
	maxLong = -9999
	for place_raw in places_raw:
		new_place = {}
		new_place['latitude'] = float(place_raw['latitude'])
		new_place['longitude'] = float(place_raw['longitude'])
		new_place['zipcode'] = int(place_raw['postcode'])
		places.append(new_place)

		minLat = min(minLat, new_place['latitude'])
		minLong = min(minLong, new_place['longitude'])
		maxLat = max(maxLat, new_place['latitude'])
		maxLong = max(maxLong, new_place['longitude'])
	
	minLat -= 0.01
	minLong -= 0.01
	maxLat += 0.01
	maxLong += 0.01

	latSlices = np.linspace(minLat, maxLat, size_n)
	longSlices = np.linspace(minLong, maxLong, size_n)

	hot_spot_grid = np.zeros((size_n, size_n))
	influence_normal_rv = norm(loc = 0, scale = influence_range_in_meter)

	# place 
	for i_lat in range(size_n):
		for j_long in range(size_n):
			for place in places:
				distance_in_km = _haversine(place['longitude'], place['latitude'], longSlices[j_long], latSlices[i_lat])
				distribution_value = influence_normal_rv.pdf(distance_in_km * 1000)
				hot_spot_grid[i_lat][j_long] += distribution_value * zip_to_population[str(place['zipcode'])]
				# print dist, distribution_value, hot_spot_grid[i_lat][j_long]

	scores = {}
	scores['data'] = []
	total_score = np.sum(hot_spot_grid)
	total_value = len(places) * SINGLE_DRINK_PRICE * DRINKS_SOLD_PER_STORE_PER_DAY
	for i_lat in range(size_n):
		for j_long in range(size_n):
			new_score_entry = {}
			new_score_entry['latitude'] = latSlices[i_lat]
			new_score_entry['longitude'] = longSlices[j_long]
			new_score_entry['score'] = hot_spot_grid[i_lat][j_long]*1.0/total_score
			new_score_entry['dollar_per_hour'] = new_score_entry['score'] * total_value / DAILY_ACTIVE_HOUR
			new_score_entry['estimated_travel_time'] = _haversine(longitude, latitude, longSlices[j_long], latSlices[i_lat]) / 5 * 60.0
			scores['data'].append(new_score_entry)

	return json.dumps(scores)
	# return 

def get_neighbors(latitude, longitude, radius=DEFAULT_RADIUS):
	attached = '&filters={"category_ids":{"$includes_any":' + str(PLACE_TYPE) + '}}&geo={"$circle":{"$center":[' + str(latitude) + ', ' + str(longitude) + '],"$meters":' + str(radius) + '}}'
	request_link = BASE_API_LINK + attached
	print request_link
	content = requests.get(request_link).content
	data = json.loads(content)['response']['data']
	return data
