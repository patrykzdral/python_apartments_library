import unittest

import exception
from google_addon.CitySearch import GoogleSearcher
from library.GeographicalLocation import GeographicalLocation
from library.Valuation import Valuation


class TestSimple(unittest.TestCase):


    def test_address_not_found(self):
        calc = GoogleSearcher()
        list_Of_available_cities = [
            "Wrocław", "Warszawa", "Kraków",
            "Gdańsk", "Katowice", "Lublin", "Łódź",
            "Poznań"]
        with self.assertRaises(
                exception.cityNotFoundException.CityNotFoundException) as context:
            calc.geocode("Płock", list_Of_available_cities)
        self.assertTrue('NIE ZNALEZIONO ADRESU' in str(context.exception))

    def test_market_not_exists(self):
        valuation = Valuation()

        with self.assertRaises(exception.marketNotExistException.MarketNotExistsException) as context:
            valuation.estimate_cost_of_the_flat(51.094053, 16.983384,
                                                120, "Wrocław",
                                                2005, False,
                                                False, False, False, False,
                                                False, False, False, False,
                                                False, "nie istnieje")
        self.assertTrue('Rynek nie istnieje' in str(context.exception))

    def test_value_error(self):
        valuation = Valuation()

        with self.assertRaises(exception.illegalArgumentException.IllegalArgumentException) as context:
            valuation.estimate_cost_of_the_flat(51.094053, 16.983384,
                                                    -120, "Wrocław",
                                                    2005, False,
                                                    False, False, False, False,
                                                    False, False, False, False,
                                                    False, "wtórny")

        self.assertTrue('Parametry wejściowe nie mogą mieć wartości ujemnej' in str(context.exception))

    def test_correct_distance(self):
        geographical = GeographicalLocation(51.094053, 16.983384)
        second_geographical = GeographicalLocation(52.188200, 20.947594)
        self.assertEqual(float("{:.2f}".format(geographical.distance_to(second_geographical))), 299336.37)

    def test_correct_additional_amenities(self):
        valuation = Valuation()

        price_before_change_construction_year = valuation.estimate_cost_of_the_flat(51.094053, 16.983384,
                                                                                    120, "Wrocław",
                                                                                    2006, False,
                                                                                    False, False, False, False,
                                                                                    False, False, False, False,
                                                                                    False, "wtórny")
        price_after_change_construction_year = valuation.estimate_cost_of_the_flat(51.094053, 16.983384,
                                                                                   120, "Wrocław",
                                                                                   2006, False,
                                                                                   False, False, False, False,
                                                                                   False, False, True, True,
                                                                                   True, "wtórny")
        self.assertEqual(float(price_before_change_construction_year) + 9000,
                         float(price_after_change_construction_year))

    def test_correct_construction_year(self):
        valuation = Valuation()

        price_before_change_construction_year = valuation.estimate_cost_of_the_flat(51.094053, 16.983384,
                                                                                    100, "Wrocław",
                                                                                    1998, False,
                                                                                    False, False, False, False,
                                                                                    False, False, False, False,
                                                                                    False, "wtórny")
        price_after_change_construction_year = valuation.estimate_cost_of_the_flat(51.094053, 16.983384,
                                                                                    100, "Wrocław",
                                                                                    2006, False,
                                                                                    False, False, False, False,
                                                                                    False, False, False, False,
                                                                                    False, "wtórny")
        self.assertEqual(float(price_before_change_construction_year),
                         float(price_after_change_construction_year)*0.9)


if __name__ == '__main__':
    unittest.main()
