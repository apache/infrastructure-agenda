import flask

app = flask.current_app

@app.route("/")
def index():
    return "HOME"