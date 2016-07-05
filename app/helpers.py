import os
import numpy as np
from app import db
from models import Activity
from sklearn.externals import joblib
basedir = os.path.abspath(os.path.dirname(__file__))

def process_and_insert_data(data):
    # turn user_info into list of format:
    # ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
    try:
        curr_health_score = calc_health_score(to_float(data.get('steps')), to_float(data.get('total_sleep')), to_float(data.get('resting_hr')))
        ml_fields = [ 'steps',
                      'total_sleep',
                      'resting_hr',
                      'step_week_slope',
                      'sleep_week_slope',
                      'hr_week_slope' ]
        ml_input = []
        for field in ml_fields:
            if data.get(field)!=0:
                ml_input.append(to_float(data.get(field)))
            else:
                return 'Data is missing'
        ml_input.append(curr_health_score)
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
            curr_health_score=to_float(curr_health_score),
            health_score_in_week=prediction
        )
        db.session.add(model_data)
        db.session.commit()
        data = {
            'prediction': prediction,
            'curr_health_score': curr_health_score
        }
        return data
    except:
        return

def calc_health_score(steps, sleep, hr):
    # data taken from training set
    steps_97th = 14929.5811883
    steps_3rd = 322.091611053
    steps_range = steps_97th - steps_3rd
    steps_weight = 0.4
    sleep_97th = 12.3114328915
    sleep_3rd = 3.6839611684
    sleep_range = sleep_97th - sleep_3rd
    sleep_weight = 0.2
    hr_97th = 76.7614950684
    hr_3rd = 60.8424882753
    hr_range = hr_97th - hr_3rd
    hr_weight = 0.4
    steps_score = np.subtract(steps, steps_3rd) / steps_range
    sleep_score = np.subtract(sleep, sleep_3rd) / sleep_range
    hr_score = 1 - (np.subtract(hr, hr_3rd) / hr_range)
    health_score = ((steps_score*steps_weight) + (sleep_score*sleep_weight) + (hr_score*hr_weight))*100
    return health_score


def make_prediction(input):
    ml_alg = joblib.load(os.path.join(basedir, 'health_prediction.pkl'))
    output = ml_alg.predict(input)
    return output[0]

def to_float(input):
    return float(input)

def to_str(input):
    return input.encode('ascii','ignore')
