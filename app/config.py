import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'fitomo'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASSWORD'] + '@predictionServiceDB:5432/predictionServiceDB'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/prediction'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
