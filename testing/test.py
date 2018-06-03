import unittest

import exception
from google_addon.CitySearch import GoogleSearcher


class TestStringMethods(unittest.TestCase):

    def test_too_small_value_of_year(self):
        calc = GoogleSearcher()

        with self.assertRaises(
                exception.cityNotFoundException.CityNotFoundException) as context:
            calc.geocode("Wrocław",["Warszawa"])

        self.assert_
        # self.assertTrue(
        #     'NIE ZNALEZIONO ADRESU' in str(context.exception))