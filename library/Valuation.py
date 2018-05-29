from library import GeographicalLocation


class Valuation:
    cost = 0
    CENTER_OF_WROCLAW = GeographicalLocation.GeographicalLocation(
        51.110516, 17.033514)
    CENTER_OF_WARSAW = GeographicalLocation.GeographicalLocation(
        52.2297700, 21.0117800)
    CENTER_OF_CRACOW = GeographicalLocation.GeographicalLocation(
        50.0614300, 19.9365800)
    CENTER_OF_GDANSK = GeographicalLocation.GeographicalLocation(
        54.3520500, 18.6463700)
    CENTER_OF_KATOWICE = GeographicalLocation.GeographicalLocation(
        50.2584100, 19.0275400)
    CENTER_OF_LUBLIN = GeographicalLocation.GeographicalLocation(
        51.2500000, 22.5666700)
    CENTER_OF_LODZ = GeographicalLocation.GeographicalLocation(
        51.7500000, 19.4666700)
    CENTER_OF_POZNAN = GeographicalLocation.GeographicalLocation(
        52.4069200, 16.9299300)
    CENTER_OF_SZCZECIN = GeographicalLocation.GeographicalLocation(
        53.4289400, 14.5530200)

    def __init__(self):

        self.list_Of_additional_amenities = [
            "basen", "siłownia", "pralnia", "piwnica"]
        self.list_Of_available_cities = [
            "Wrocław", "Warszawa", "Kraków",
            "Gdańsk", "Katowice", "Lublin", "Łódź",
            "Poznań", "Szczecin"]

    def get_cost(self, square_meters, sq1, sq2, sq3, distance):
        if square_meters < 38:
            cost = sq1 * square_meters
        elif square_meters < 60:
            cost = sq2 * square_meters
        else:
            cost = square_meters * sq3

        if distance < 1000:
            cost *= 1.2
        elif distance < 2000:
            cost *= 1.1
        elif distance < 3000:
            cost *= 1.0
        elif distance < 4000:
            cost *= 0.9
        elif distance < 5000:
            cost *= 0.8
        return cost

    def estimate_cost_of_the_flat(self, latitude, longitude,
                                  square_meters, city,
                                  construction_year, furnished,
                                  balcony, usable_room, garage, cellar,
                                  garden, patio, elevator, two_floors,
                                  air_conditioning, market):
        self.cost = 0
        city.lower()
        cost = self.numbers_to_strings(
            city, square_meters, market, latitude, longitude)
        cost = float(cost)
        if garage:
            cost += 15000
        if furnished:
            cost *= 1.15
        if balcony:
            cost += 5000
        if patio:
            cost += 5000
        if elevator:
            cost += 1000
        if two_floors:
            cost += 5000
        if air_conditioning:
            cost += 3000
        if usable_room:
            cost += 150
        if cellar:
            cost += 5000
        if garden:
            cost += 5000

        if construction_year < 2000:
            cost *= 0.9
        elif construction_year < 2005:
            cost *= 0.95
        elif 2010 < construction_year < 2015:
            cost *= 1.05
        else:
            cost *= 1.1

        return "{0:.2f}".format(round(cost, 2))

    def numbers_to_strings(self, city, square_meters,
                           market, latitude, longitude):

        city = city.lower()
        print(city)
        if market == "pierwotny":
            switcher = {
                "wrocław": Valuation.get_info(
                    self, square_meters,
                    7032, 6217, 6118, latitude,
                    longitude, self.CENTER_OF_WROCLAW),
                "warszawa": Valuation.get_info(
                    self, square_meters,
                    7841, 7660, 7895, latitude,
                    longitude, self.CENTER_OF_WARSAW),
                "kraków": Valuation.get_info(
                    self, square_meters,
                    7990, 7085, 7482, latitude,
                    longitude, self.CENTER_OF_CRACOW),
                "gdańsk": Valuation.get_info(
                    self, square_meters,
                    8667, 5998, 6773, latitude,
                    longitude, self.CENTER_OF_CRACOW),
                "katowice": Valuation.get_info(
                    self, square_meters,
                    5472, 5364, 5425, latitude,
                    longitude, self.CENTER_OF_KATOWICE),
                "lublin": Valuation.get_info(
                    self, square_meters,
                    5824, 5486, 5235, latitude,
                    longitude, self.CENTER_OF_LUBLIN),
                "łódź": Valuation.get_info(
                    self, square_meters,
                    5567, 5200, 4891, latitude,
                    longitude, self.CENTER_OF_LODZ),
                "poznań": Valuation.get_info(
                    self, square_meters,
                    7217, 6377, 6290, latitude, longitude,
                    self.CENTER_OF_POZNAN),
                "szczecin": Valuation.get_info(
                    self, square_meters,
                    5254, 5095, 5120, latitude, longitude,
                    self.CENTER_OF_SZCZECIN)
            }
        else:
            switcher = {
                "wrocław": self.get_info(
                    square_meters,
                    7442, 6639, 6177, latitude,
                    longitude, self.CENTER_OF_WROCLAW),
                "warszawa": Valuation.get_info(
                    self, square_meters,
                    9865, 8969, 9010, latitude,
                    longitude, self.CENTER_OF_WARSAW),
                "kraków": Valuation.get_info(
                    self, square_meters,
                    9040, 7623, 7508, latitude,
                    longitude, self.CENTER_OF_CRACOW),
                "gdańsk": Valuation.get_info(
                    self, square_meters,
                    8700, 8632, 7572, latitude,
                    longitude, self.CENTER_OF_CRACOW),
                "katowice": Valuation.get_info(
                    self, square_meters,
                    5051, 4525, 4652, latitude,
                    longitude, self.CENTER_OF_KATOWICE),
                "lublin": Valuation.get_info(
                    self, square_meters,
                    5855, 5211, 5110, latitude,
                    longitude, self.CENTER_OF_LUBLIN),
                "łódź": Valuation.get_info(
                    self, square_meters,
                    3997, 4304, 4480, latitude,
                    longitude, self.CENTER_OF_LODZ),
                "poznań": Valuation.get_info(
                    self, square_meters,
                    6999, 6433, 5948, latitude,
                    longitude, self.CENTER_OF_POZNAN),
                "szczecin": Valuation.get_info(
                    self, square_meters,
                    5502, 4909, 4711, latitude,
                    longitude, self.CENTER_OF_SZCZECIN)
            }
        return switcher.get(city, "nothing")

    def get_info(self, square_meters, sq1, sq2,
                 sq3, latitude, longitude, lat_lon_city):
        print(latitude)
        print(longitude)
        print(lat_lon_city)
        distance = GeographicalLocation.GeographicalLocation(
            latitude, longitude).distance_to(lat_lon_city)
        cost = self.get_cost(square_meters, sq1, sq2, sq3, distance)
        return cost
