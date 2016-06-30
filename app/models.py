from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    steps = db.Column(db.Float)
    user_id = db.Column(db.String)
    total_sleep = db.Column(db.Float)
    resting_hr = db.Column(db.Float)
    step_week_slope = db.Column(db.Float)
    sleep_week_slope = db.Column(db.Float)
    hr_week_slope = db.Column(db.Float)
    curr_health_score = db.Column(db.Float)
    health_score_in_week = db.Column(db.Float)

    def __init__(self, date, steps, user_id,
                total_sleep, resting_hr,
                step_week_slope, sleep_week_slope,
                hr_week_slope, curr_health_score,
                health_score_in_week):
                    self.date = date
                    self.steps = steps
                    self.user_id = user_id
                    self.total_sleep = total_sleep
                    self.resting_hr = resting_hr
                    self.step_week_slope = step_week_slope
                    self.sleep_week_slope = sleep_week_slope
                    self.hr_week_slope = hr_week_slope
                    self.curr_health_score = curr_health_score
                    self.health_score_in_week = health_score_in_week

    def __repr__(self):
        return '<id {}>'.format(self.id)
