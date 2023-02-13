import os
import random
import string

basedir = os.path.dirname(__file__)

class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or ''.join([random.choice(string.ascii_letters + string.ascii_lowercase + string.digits + string.punctuation ) for n in range(128)])
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Recipes REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

class DevConfig(BaseConfig):
    PORT = 8080
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///'+os.path.join(basedir+'/dev-db.sqlite')

class TestConfig(BaseConfig):
    PORT = 8081
    DEBUG = True
    TESTING = True
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///'+os.path.join(basedir+'/testing-db.sqlite')

class ProdConfig(BaseConfig):
    PORT = 80
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


config = {
    'production': ProdConfig,
    'development': DevConfig,
    'testing': TestConfig,
    'default': DevConfig
}