import googlemaps

from exception.cityNotFoundException import CityNotFoundException


class GoogleSearcher(object):
    gmaps = None

    def __init__(self):
        self.gmaps = googlemaps.Client(
            key='AIzaSyAWPy2RuBxzziKOgEDLXa2LrXakMIHlBpY')

    def find_city(self, geocode_result, list):
        found = False
        City = None
        for i in range(0, len(geocode_result['address_components'])):
            for x in geocode_result['address_components'][i]:
                if x == "long_name":
                    locality = geocode_result[
                        'address_components'][i]['long_name']
                    if list.__contains__(locality):
                        City=locality
                        found = True

        if not found:
            raise (CityNotFoundException("NIE ZNALEZIONO ADRESU"))
        return [found, City]

    def geocode(self, text, list):
        geocode_result = self.gmaps.geocode(
            'Poland ' + text)[0]
        self.latitude = geocode_result['geometry']['location']['lat']
        self.longitude = geocode_result['geometry']['location']['lng']
        return [self.find_city(geocode_result, list),geocode_result]
