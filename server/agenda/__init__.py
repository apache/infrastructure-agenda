import flask
import flask_bootstrap

# from config import config

bootstrap = flask_bootstrap.Bootstrap()


def create_app(config_name):
    app = flask.Flask('agenda')
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    bootstrap.init_app(app)

    from . import converters
    app.url_map.converters['meeting_dates'] = converters.DateConverter

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
