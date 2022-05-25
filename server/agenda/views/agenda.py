import flask

app = flask.current_app

@app.route("/agendas")
def agendas_index():
    return "AGENDAS!"