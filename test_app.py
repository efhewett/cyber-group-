import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', result.data)

    def test_nasa_photo(self):
        result = self.app.get('/nasa-photo')
        self.assertIn(result.status_code, [200, 404])

    def test_aurora_watch(self):
        result = self.app.get('/aurora-watch')
        self.assertIn(result.status_code, [200, 500])

    def test_nasa_geostorm(self):
        result = self.app.get('/nasa-geostorm')
        self.assertIn(result.status_code, [200, 404])

    def test_plot_png(self):
        result = self.app.get('/plot.png')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.mimetype, 'image/png')

if __name__ == "__main__":
    unittest.main()
