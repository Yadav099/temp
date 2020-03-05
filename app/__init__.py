from config import app_config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

def create_app(config_name):
    APP = Flask(__name__, instance_relative_config=True)
    APP.config.from_object(app_config[config_name])
    APP.debug = True
    return APP


APP = create_app('config')
bcrypt = Bcrypt(APP)

DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB, compare_type=True)


from app import routes, models