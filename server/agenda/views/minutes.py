import flask

from . import tools
from ..models import minutes

app = flask.current_app
minutes = minutes.Minutes()

T_MINUTES = tools.load_template('minutes.html.ezt')


@app.route("/minutes")
def minutes_index():

    items = minutes.get_all()
    data = {'title': 'Minutes',
            'items': items,
    }

    return tools.render(T_MINUTES, data)

@app.route("/minutes/<date:meeting_date>")
def find_minutes(meeting_date):
    return minutes.get_by_date(meeting_date).contents
