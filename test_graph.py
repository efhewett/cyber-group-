import unittest
from graph import SolarFlare, GeoStorm, get_sf_data, get_gms_data

class TestGraph(unittest.TestCase):

    def test_solar_flare_activity_level(self):
        flare = SolarFlare(class_type="X1", peak_time="2024-01-01 00:00:00")
        activity_level = flare.get_activity_level()
        self.assertEqual(activity_level, 9)

    def test_geo_storm_activity_level(self):
        storm = GeoStorm(obs_time="2024-01-01 00:00:00", kp_index=5)
        activity_level = storm.get_activity_level()
        self.assertEqual(activity_level, 5)

    def test_get_sf_data(self):
        flares = get_sf_data()
        self.assertIsInstance(flares, list)

    def test_get_gms_data(self):
        storms = get_gms_data()
        self.assertIsInstance(storms, list)

if __name__ == "__main__":
    unittest.main()
