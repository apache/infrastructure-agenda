import os

APP_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATA_DIR = os.getenv('DATA_DIR') or os.path.join(APP_DIR, 'data')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    DATA_DIR = os.path.join(APP_DIR, 'tests', 'data')
    TESTING = True


class ProductionConfig(Config):
    pass
