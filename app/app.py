import os
import json
from flask import Flask, request, Response
from models import db
import config

app = Flask(__name__)
# Set config
app.config.from_object(os.environ['APP_SETTINGS'])
# Initialize app
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
            # Put data through algorithm and insert into database
            data = process_and_insert_data(request.args)
            # Turn data into json format
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
