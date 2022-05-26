import flask

from . import api
from server.agenda.models import agenda


agendas = agenda.Agenda()


@api.route('/agendas')
def get_all_agendas():
    items = agendas.get_all()
    return flask.jsonify(items=items, count=len(items))


@api.route('/agendas/<meeting_dates:date>')
def get_agenda_by_date(date):
    item = agendas.get_by_date(date)

    return flask.jsonify(items=item.info, count=1)
