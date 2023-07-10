"""config.py"""

import os
from dotenv import load_dotenv

import sqlalchemy

from sqlalchemy.engine.url import make_url
from supabase import create_client, Client

basedir = os.path.abspath(os.path.dirname(__file__))


load_dotenv()

# url = make_url(engine.url)


class Config():
    """main config"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    """production config"""
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    DEBUG = False
    DEVELOPMENT = True


class StagingConfig(Config):
    """staging config"""
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """development config"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """testing config"""
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'staging': StagingConfig
}
