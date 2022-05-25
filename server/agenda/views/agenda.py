import flask

from . import tools
from .. import models

app = flask.current_app
agendas = models.Agenda()

T_AGENDAS = tools.load_template('agendas.html.ezt')


@app.route("/agendas")
def agendas_index():

    items = agendas.get_all()
    formatted_items = [item[0] for item in items]
    data = {'title': 'List of Agendas',
            'items': formatted_items
    }

    return tools.render(T_AGENDAS, data)
