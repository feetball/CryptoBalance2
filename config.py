# config.py
import datetime
import logging

class Config(object):
    """
    Common configurations
    """
    DEBUG = True
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'CryptoBalance.log'

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Production configurations
    """
    LOGGING_LEVEL = logging.ERROR
    DEBUG = False

class TestingConfig(Config):
    """
    Testing configurations
    """
    LOGGING_LEVEL = logging.INFO
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
