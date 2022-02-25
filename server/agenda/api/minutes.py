import flask

from . import api
from ..models import Minutes


minutes = Minutes()


@api.route('/minutes')
def get_all_minutes():
    items = minutes.get_all_minutes()
    return flask.jsonify(items=items, count=len(items))


@api.route('/minutes/<meeting_dates:date>')
def get_minutes_by_date(date):
    item = minutes.get_minutes_by_date(date)

    return flask.jsonify(items=item.info, count=1)
