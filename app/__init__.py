
from flask_mail import Mail

from config import app_config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
from flask_jwt_extended import JWTManager


def create_app(config_name):
    APP = Flask(__name__, instance_relative_config=True)
    run_with_ngrok(APP)
    APP.config.from_object(app_config[config_name])
    APP.debug = True
    CORS(APP)
    return APP


APP = create_app('config')
run_with_ngrok(APP)

APP.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(APP)

# <<<<<<< HEAD
APP.config['DEBUG'] = True
APP.config['TESTING'] = False
APP.config['MAIL_SERVER'] = 'smtp.gmail.com'
APP.config['MAIL_PORT'] = 587
APP.config['MAIL_USE_TLS'] = True
APP.config['MAIL_USE_SSL'] = False
APP.config['MAIL_USERNAME'] = 'smartcommhu17@gmail.com'
APP.config['MAIL_PASSWORD'] = 'qwerty@123'
APP.config['MAIL_DEFAULT_SENDER'] = 'smartcommhu17@gmail.com'
APP.config['MAIL_ASCII_ATTACHMENTS'] = False

# =======
# >>>>>>> 8340faaab433f73d1db6049982ff0c215ced6cc7

bcrypt = Bcrypt(APP)

mail = Mail(APP)
DB = SQLAlchemy(APP)
METADATA = DB.MetaData()
MIGRATE = Migrate(APP, DB, compare_type=True)

from app import routes, models


# sudo -u postgres psql smartcomm
