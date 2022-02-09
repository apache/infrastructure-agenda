from . import api


@api.route('/agendas')
def get_agendas():
    pass


@api.route('/agendas/<meeting_dates:date>')
def get_agenda(date):
    pass
