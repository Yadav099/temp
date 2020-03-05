from flask import Flask

APP = Flask(__name__)
APP.debug = True


from app import routes, models