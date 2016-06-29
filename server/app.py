import os
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/classification'

app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def import_models():
    from models import Activity

@app.route('/')
def intro():
    return 'Hello!'

if __name__ == '__main__':
    app.run()
