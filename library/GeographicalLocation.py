import math


class GeographicalLocation(object):

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, geographical_location):
        r = 6371
        lat_distance = math.radians(geographical_location.latitude
                                    - self.latitude)
        lon_distance = math.radians(geographical_location.longitude
                                    - self.longitude)
        a = math.sin(lat_distance / 2) * math.sin(lat_distance / 2) \
            + math.cos(math.radians(self.latitude)) * \
            math.cos(math.radians(geographical_location.latitude)) \
            * math.sin(lon_distance / 2) \
            * math.sin(lon_distance / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = r * c * 1000
        return distance
