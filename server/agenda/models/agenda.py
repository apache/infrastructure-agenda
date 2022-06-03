import os
import datetime

import flask

from agenda.utils import svn


class Agenda(object):

    def __init__(self):
        self._dir = svn.Dir(os.path.join(flask.current_app.config['DATA_DIR'],
                                         'repos',
                                         'foundation_board'),
                            filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                            recurse=True)

    def get_all(self):
        agendas = self._dir.files
        # TODO: this only works the first time the agendas index page is displayed
        #       because it changes the underlying objects. So check before changing
        #       or do this differently.
        for agenda in agendas:
            dt = self._parse_date_from_name(agenda.filename)
            agenda.name = dt.strftime("%a, %d %b %Y")
            agenda.url = flask.url_for('find_agenda', meeting_date=dt)
            agenda.last_changed_date = agenda.last_changed_date.strftime("%c")
            agenda.minutes = self._minutes_filename(agenda.filename)
            agenda.minutes_url = flask.url_for('find_minutes', meeting_date=dt)
        return agendas

    def get_by_date(self, date):
        filename = f"board_agenda_{date.strftime('%Y_%m_%d')}.txt"

        return self._dir.file(filename)

    # TODO: move these to shared module so that we can import into other models
    @staticmethod
    def _parse_date_from_name(fname):
        fname_cleaned = fname.rstrip(".txt").split("_")[2:]
        return datetime.date(*[int(element) for element in fname_cleaned])

    @staticmethod
    def _minutes_filename(fname):
        return fname.replace('board_agenda', 'board_minutes')

