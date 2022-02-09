import flask
from . import api


@api.route('/reports')
def get_reports():
    pass


@api.route('/reports/<int:id>')
def get_report(id):
    pass


@api.route('/reports/', methods=['POST'])
# need to figure out permissions scheme
def new_report():
    pass


@api.route('/reports/<int:id>', methods=['PUT'])
def edit_report(id):
    pass
