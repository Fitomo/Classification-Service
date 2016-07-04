import os
import sys
import unittest
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.insert(0, parentdir)

from app.app import app, db
from app.models import Activity
from app.config import TestingConfig
os.environ['APP_SETTINGS'] = 'TestingConfig'

class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        result = self.app.get('/')
        self.assertEqual(result.data, 'You\'ve reached the Fitomo prediction service')

    def test_api_status_code(self):
        result = self.app.get('/api/getPrediction')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
