import flask

from . import tools

app = flask.current_app

T_HOME = tools.load_template('home.html.ezt')


@app.route("/")
def index():
    data = {'title': "Welcome",
    }

    return tools.render(T_HOME, data)
