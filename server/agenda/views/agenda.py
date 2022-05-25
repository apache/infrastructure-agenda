import flask

from . import tools

app = flask.current_app

T_HOME = tools.load_template('home.html.ezt')


@app.route("/agendas")
def agendas_index():

    data = {'title': 'List of Agendas',
            'body': 'A list of agendas will soon appear here.',
    }

    return tools.render(T_HOME, data)
