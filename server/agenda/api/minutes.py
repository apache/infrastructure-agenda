import flask

from . import api
from ..models import Minutes


minutes = Minutes()


@api.route('/minutes')
def get_all_minutes():
    items = minutes.get_all_minutes()
    return flask.jsonify(items=items, count=len(items))
