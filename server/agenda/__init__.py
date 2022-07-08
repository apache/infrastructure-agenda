import os

import flask
import yaml


def init_app(app_dir):
    app = flask.Flask(__name__, instance_relative_config=False)

    app.config.from_file(f"{app_dir}/agenda.yaml", load=yaml.safe_load)

    from . import converters
    app.url_map.converters['date'] = converters.DateConverter

    with app.app_context():
        from . import views

        return app
