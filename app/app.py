import json
import config
from flask import Flask, request, Response
from models import db

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from helpers import *

@app.route('/')
def index():
    return 'You\'ve reached the Fitomo prediction service'

@app.route('/api/getPrediction', methods=['GET'])
def get_prediction():
    errors = []
    results = {}
    if request.method=='GET':
        try:
            data = process_and_insert_data(request.args)
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
        except:
            errors.append(
                '''Error in getting prediction.
                Make sure your request was sent correctly.
                '''
            )
    else:
        return 'Please send a get request to this api'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
