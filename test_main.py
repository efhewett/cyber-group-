import unittest
from unittest.mock import patch, MagicMock
from main import SolarFlareFetcher, GeoStormFetcher

class TestMain(unittest.TestCase):

    @patch('main.SolarFlareFetcher.fetch_data')
    def test_solar_flare_fetcher(self, mock_fetch_data):
        mock_fetch_data.return_value = [{'flrID': 'FLR1', 'classType': 'X'}]
        fetcher = SolarFlareFetcher(api_key="dummy_key")
        data = fetcher.get_flare_data('2024-01-01', '2024-01-31')
        self.assertIsNotNone(data)
        self.assertIn('flrID', data[0])

    @patch('main.GeoStormFetcher.fetch_data')
    def test_geo_storm_fetcher(self, mock_fetch_data):
        mock_fetch_data.return_value = [{'gstID': 'GST1', 'allKpIndex': [{'kpIndex': 5}]}]
        fetcher = GeoStormFetcher(api_key="dummy_key")
        data = fetcher.get_geostorm_data('2024-01-01', '2024-01-31')
        self.assertIsNotNone(data)
        self.assertIn('gstID', data[0])

if __name__ == "__main__":
    unittest.main()
