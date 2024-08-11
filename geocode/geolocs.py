import json
from .country_codes import COUNTRY_CODES

class GeoCountry:
	code = 'ZZ'
	name = 'unknown'
	code_file = ''
	code_file_template = 'geocode/geocode_{}.json'
	geolocs = []
	
	def __init__(self, code='', name=''):
		if code:
			for country_name, country_code in COUNTRY_CODES.items():
				if code == country_code:
					self.code = country_code
					self.name = country_name
					break
		elif name:
			for country_name, country_code in COUNTRY_CODES.items():
				if name == country_name:
					self.code = country_code
					self.name = country_name
					break
		self.populate_code_file()
		self.load_geolocs_from_file()
		
	def populate_code_file(self):
		if self.code and self.code != 'ZZ':
			self.code_file = self.code_file_template.format(self.code)
		
	def load_geolocs_from_file(self):
		if self.code_file:
			self.geolocs = []
			with open(self.code_file, encoding='utf-8') as f:
				data = json.load(f)
				for geoloc_data in data:
					geoloc = GeoLoc(geoloc_data)
					self.geolocs.append(geoloc)
				
	def states(self):
		try:
			return list(set(sorted([loc.state for loc in self.geolocs])))
		except Exception:
			return []
				
	def cities(self, state=None):
		try:
			if state:
				return list(set(sorted([loc.city for loc in self.geolocs if state == loc.state])))
			return list(set(sorted([loc.city for loc in self.geolocs])))
		except Exception:
			return []
		
	def locations(self):
		return list(set(sorted([loc.__repr__() for loc in self.geolocs])))
		
	def get_geo_loc(self, state, city):
		geo_loc = None
		for loc in self.geolocs:
			if loc.state == state and loc.city == city:
				geo_loc = loc
				break
			if not state and loc.city == city:
				geo_loc = loc
				break
		return geo_loc

	def __repr__(self):
		return '{}: {} [{}]'.format(self.name, self.code, self.code_file)

class GeoLoc:
	state = 'unknown_state'
	city = 'unknown_city'
	latitude = 0.0
	longitude = 0.0
	
	def __init__(self, json_data):
		self.state = json_data.get('state')
		self.city = json_data.get('city')
		self.latitude = json_data.get('latitude')
		self.longitude = json_data.get('longitude')
		
	def __repr__(self):
		return '{}: {}'.format(self.state, self.city)
	

if __name__ == '__main__':
	gc = GeoCountry('US')
	