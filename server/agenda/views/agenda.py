import flask

from . import tools
from ..models import agenda

app = flask.current_app
agendas = agenda.Agenda()

T_AGENDAS = tools.load_template('agendas.html.ezt')


@app.route("/agendas")
def agendas_index():

    items = agendas.get_all()
    data = {'title': 'Agendas',
            'page_name': 'agendas',
            'items': items,
    }

    return tools.render(T_AGENDAS, data)
