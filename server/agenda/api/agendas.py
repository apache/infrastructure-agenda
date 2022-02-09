import flask

from . import api
from ..models import Agenda


@api.route('/agendas')
def get_agendas():
    return flask.jsonify(Agenda.get_files())


@api.route('/agendas/<meeting_dates:date>')
def get_agenda(date):
    pass
