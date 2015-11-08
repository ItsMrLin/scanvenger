import os, csv
# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

def get_static(path):
	with open(os.path.join(APP_STATIC, path)) as f:
		return f.read()

def load_csv_as_dict(path):
	with open(os.path.join(APP_STATIC, path), mode='r') as infile:
		reader = csv.reader(infile)
		mydict = {rows[0]:int(rows[1]) for rows in reader}
	return mydict