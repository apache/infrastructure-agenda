import flask

from . import api
from ..models import Agenda


agendas = Agenda()


@api.route('/agendas')
def get_all_agendas():
    items = agendas.get_all_agendas()
    return flask.jsonify(items=items, count=len(items))


@api.route('/agendas/<meeting_dates:date>')
    pass
def get_agenda_by_date(date):
