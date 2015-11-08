#settings.py
import os
# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

def get_static(path):
	with open(os.path.join(APP_STATIC, path)) as f:
		return f.read()