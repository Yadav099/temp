import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'sqlite:///' + \
        os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DEBUG = True
    TESTING = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 585
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'smartcommhu17@gmail.com'
    MAIL_PASSWORD = 'qwerty@123'
    MAIL_DEFAULT_SENDER = 'smartcommhu17@gmail.com'
    MAIL_ASCII_ATTACHMENTS = False


app_config = {
    'config': Config
}
