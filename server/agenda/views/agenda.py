import flask

from . import tools
from ..models import agenda

app = flask.current_app
agendas = agenda.AgendaList(app.config['AGENDA_REPO'])

T_AGENDAS = tools.load_template('agendas.html.ezt')
T_AGENDA = tools.load_template('agenda.html.ezt')


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

    item = agendas.get_by_date(meeting_date)

    data = {'title': f"Meeting Agenda for {item.name}",
            'meeting_date': item.name,
            'start_time': item.parsed_file.call_to_order[0],
            'time_zone_link': item.parsed_file.call_to_order[1],
            'directors_present': item.parsed_file.roll_call[0],
            'directors_absent': item.parsed_file.roll_call[1],
            'officers_present': item.parsed_file.roll_call[2],
            'officers_absent': item.parsed_file.roll_call[3],
            'guests': item.parsed_file.roll_call[4],
            'minutes': item.parsed_file.last_minutes
            }

    return tools.render(T_AGENDA, data)
