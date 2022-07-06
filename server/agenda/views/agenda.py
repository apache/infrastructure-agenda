import flask

from . import tools
from ..models import agenda

app = flask.current_app
agendas = agenda.AgendaList(app.config['DATA_DIR'])

T_AGENDAS = tools.load_template('agendas.html.ezt')


@app.route("/agendas")
def agendas_index():

    items = agendas.get_all()
    for a in items:
        a.url = flask.url_for('find_agenda', meeting_date=a.date)
        a.minutes_url = '#' # TODO: these two lines will be updated when models.Minutes is re-implemented
        a.minutes = ''

    sort = flask.request.args.get('sort')
    if sort == 'forward':
        items.sort()
    else:
        items.sort(reverse=True)

    data = {'title': 'Agendas',
            'count': len(items),
            'items': items,
    }

    return tools.render(T_AGENDAS, data)

@app.route("/agendas/<date:meeting_date>")
def find_agenda(meeting_date):
    return agendas.get_by_date(meeting_date).name
