import flask


def init_app():
    app = flask.Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.TestingConfig') # TODO: change this to be set by ENV variables

    from . import converters
    app.url_map.converters['date'] = converters.DateConverter

    with app.app_context():
        from . import views

        return app
