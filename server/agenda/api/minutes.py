import flask

from . import api
from ..models import Minutes


@api.route('/minutes')
def get_minutes():
    return flask.jsonify(Minutes.get_files())
