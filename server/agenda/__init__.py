import flask

import config


def init_app(cfg=config.DevelopmentConfig):
    app = flask.Flask(__name__, instance_relative_config=False)
    app.config.from_object(cfg)

    from . import converters
    app.url_map.converters['date'] = converters.DateConverter

    with app.app_context():
        from . import views

        return app
