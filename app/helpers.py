import os
from app import db
from models import Activity
from sklearn.externals import joblib
basedir = os.path.abspath(os.path.dirname(__file__))

def process_and_insert_data(data):
    # turn user_info into list of format:
    # ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
    ml_fields = [ 'steps',
                  'total_sleep',
                  'resting_hr',
                  'step_week_slope',
                  'sleep_week_slope',
                  'hr_week_slope',
                  'curr_health_score' ]
    ml_input = []
    for field in ml_fields:
        if data.get(field)!=0:
            ml_input.append(to_float(data.get(field)))
        else:
            return 'Data is missing'
    prediction = make_prediction(ml_input)
    model_data = Activity(
        date=to_str(data.get('date')),
        steps=to_float(data.get('steps')),
        user_id=to_str(data.get('user_id')),
        total_sleep=to_float(data.get('total_sleep')),
        resting_hr=to_float(data.get('resting_hr')),
        step_week_slope=to_float(data.get('step_week_slope')),
        sleep_week_slope=to_float(data.get('sleep_week_slope')),
        hr_week_slope=to_float(data.get('hr_week_slope')),
        curr_health_score=to_float(data.get('curr_health_score')),
        health_score_in_week=prediction
    )
    db.session.add(model_data)
    db.session.commit()
    return prediction

def make_prediction(input):
    ml_alg = joblib.load(os.path.join(basedir, 'health_prediction.pkl'))
    output = ml_alg.predict(input)
    return output[0]

def to_float(input):
    return float(input)

def to_str(input):
    return input.encode('ascii','ignore')
