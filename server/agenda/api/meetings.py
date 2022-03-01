import flask

from . import api
from ..models import Meeting


meetings = Meeting()


@api.route('/meetings')
def get_all_meetings():
    items = meetings.get_all()
    return flask.jsonify(items=items, count=len(items))


@api.route('/meetings/next')
def get_next_meeting():
    items = meetings.get_next()
    return flask.jsonify(items=items, count=len(items))


@api.route('/meetings/prev')
def get_prev_meeting():
    items = meetings.get_prev()
    return flask.jsonify(items=items, count=len(items))


@api.route('/meetings/<int:year>/<int:month>')
def get_meeting_by_month(year, month):
    items = meetings.get_by_month(year, month)
    return flask.jsonify(items=items, count=len(items))
