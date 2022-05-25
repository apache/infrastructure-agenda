import flask


def init_app():
    app = flask.Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevelopmentConfig') # TODO: change this to be set by ENV variables

    with app.app_context():
        from . import views

        return app
