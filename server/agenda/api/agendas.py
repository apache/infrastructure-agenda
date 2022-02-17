import flask

from . import api
from ..models import Agenda


agendas = Agenda()


@api.route('/agendas')
def get_agendas():
    items = agendas.get_agendas()
    return flask.jsonify(items=items, count=len(items))


@api.route('/agendas/<meeting_dates:date>')
def get_agenda(date):
    pass
