import flask


def init_app():
    app = flask.Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        from . import views

        return app
