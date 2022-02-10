import flask

from . import api


@api.app_errorhandler(404)
def handle_404(err):
    return flask.jsonify({'error': 'not found'}), 404
