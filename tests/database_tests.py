import os
import sys
import unittest
from sqlalchemy import create_engine
from sqlalchemy.sql import select
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.insert(0, parentdir)

from app.app import app, db
from app.models import Activity
os.environ['APP_SETTINGS'] = 'TestingConfig'

class DatabaseTests(unittest.TestCase):
    def create_app(self):
        return app

    def setUp(self):
        db.init_app(app)

    def tearDown(self):
        db.session.remove()

    def test_insertion(self):
        conn = db.connect()
        insertion = Activity(
            date='20160704',
            steps=10000,
            user_id='1',
            total_sleep=8,
            resting_hr=60,
            step_week_slope=1,
            sleep_week_slope=1,
            hr_week_slope=1,
            curr_health_score=60,
            health_score_in_week=65
        )
        s = db.select()
        result = conn.execute(s)
        print result
        self.assertEqual(result, 200)

if __name__ == '__main__':
    unittest.main()
