import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("SECRET_KEY", default="Do I really need this?")

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@localhost:5432/surfspot'
    SECRET_KEY = os.getenv("SECRET_KEY", default="Do I really need this?")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}
