import flask

from . import api
from server.agenda.models import committee


committees = committee.Committee()


@api.route('/committees')
def get_all_committees():
    items = committees.get_all()
    return flask.jsonify(items=items, count=len(items))


@api.route('/committees/<name>')
def get_committee_by_name(name):
    items = committees.get_by_name(name)
    return flask.jsonify(items=items, count=len(items))
