import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATA_DIR = os.path.join(basedir, 'tests/data')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATA_DIR = os.environ.get('DATA_DIR') or os.path.join(basedir, 'data')


class TestingConfig(Config):
    TESTING = True
    DATA_DIR = os.path.join(basedir, 'tests/data')


class ProductionConfig(Config):
    DATA_DIR = os.environ.get('DATA_DIR') or os.path.join(basedir, 'data')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
