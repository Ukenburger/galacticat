import json

# Splits geocode json file into distinct country_code json files

cc_data = {}

with open('geocode') as f:
	data = json.load(f)
	for country_data in data:
		cc = country_data.get('country_code')
		if not cc_data.get(cc):
			cc_data[cc] = []
		cc_entry = {
			'city': country_data.get('city'),
			'latitude': country_data.get('latitude'),
			'longitude': country_data.get('longitude'),
			'state': country_data.get('state')
		}
		cc_data[cc].append(cc_entry)
		
for country_code, location_data in cc_data.items():
	with open('geocode_{}.json'.format(country_code), 'w', encoding='utf-8') as f:
		f.write(json.dumps(location_data))