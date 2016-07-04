import os
import sys
import unittest
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.insert(0, parentdir)

from app.helpers import *

class HelperTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_home_status_code(self):
        result = calc_health_score(10000, 8, 60)
        self.assertEqual(result, 78.623498253393706)

if __name__ == '__main__':
    unittest.main()
