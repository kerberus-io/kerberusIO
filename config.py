import os


_basedir = os.path.abspath(os.path.dirname(__file__))


# Creates the default Config Object
class Config(object):
    # APP Settings
    DEBUG = False
    TESTING = False

    # Secrets Configuration
    SECRET_KEY = "testing_secret_key"

    TITLE = "kerberus.io"

    # Email Config
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ["MAIL_USER"]
    MAIL_PASSWORD = os.environ["MAIL_PASS"]
    MAIL_DEFAULT_SENDER = os.environ["MAIL_SEND"]
    MAIL_DEFAULT_RECEIVER = os.environ["MAIL_RECEIVE"]

    # SQLite Config
    DB_TYPE = "sqlite"  # or "postgress"
    DATABASE = os.path.join(_basedir, "kerberus.db")

    # Files Config
    UPLOAD_FOLDER = os.path.join(_basedir, "kerberusIO", "static", "img")
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf'])


# Overrides the default Config Object for Production
class ProductionConfig(Config):
    pass


# Overrides the default Config Object for Development
class DevelopmentConfig(Config):
    DEBUG = True
    pass


# Overrides the default Config Object for Testing
class TestingConfig(Config):
    TESTING = True
    pass


del os

if __name__ == '__main__':
    print(_basedir)
    print(Config.UPLOAD_FOLDER)
