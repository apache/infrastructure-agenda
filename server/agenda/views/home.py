import flask

from . import tools

app = flask.current_app

T_HOME = tools.load_template('home.html.ezt')


@app.route("/")
def index():
    data = {'title': "Home",
            'body': "This app is full of agendas.",
    }

    return tools.render(T_HOME, data)
