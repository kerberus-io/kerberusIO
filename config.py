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
