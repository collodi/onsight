import csv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#	0 name
#	1 location
#	2 url
#	3 average stars
#	4 route type
#	5 grade
#	6 pitches
#	7 length
#	8 lat
#	9 lon

def csv_to_dict(fn):
	with open(fn, newline='') as f:
		reader = csv.reader(f)
		rows = [x for x in reader]

		head, rows = rows[0], rows[1:]
		head = ['name', 'location', 'url', 'stars', 'your stars', 'type', \
				'grade', 'pitches', 'length', 'lat', 'lon']

		return [{ k: v for k, v in zip(head, row) } for row in rows]

def rm_key(d, key):
	return { k: v for k, v in d.items() if k != key }

def transform_route(route):
	route['stars'] = float(route['stars'])
	route['pitches'] = int(route['pitches'])
	route['length'] = int(route['length']) if route['length'] != '' else 0
	route['lat'] = float(route['lat'])
	route['lon'] = float(route['lon'])
	return route

def main():
	routes = csv_to_dict('sandrock.csv')
	routes = [rm_key(rt, 'your stars') for rt in routes]
	routes = [transform_route(rt) for rt in routes]

	cred = credentials.Certificate('firebase_keys/onsight_1.json')
	firebase_admin.initialize_app(cred)

	db = firestore.client()

	batch = db.batch()
	for route in routes:
		doc = db.collection(u'routes').document()
		batch.set(doc, route)

	batch.commit()

if __name__ == '__main__':
	main()
