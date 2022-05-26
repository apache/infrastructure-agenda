import os

import flask

from server.agenda.utils import svn


class Agenda(object):

    def __init__(self):
        self._dir = svn.Dir(os.path.join(flask.current_app.config['DATA_DIR'],
                                         'repos',
                                         'foundation_board'),
                            filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                            recurse=True)

    def get_all(self):

        return [[agenda.name,
                agenda['checksum'],
                agenda['last_changed_rev']]
                for agenda
                in self._dir.files]

    def get_by_date(self, date):
        filename = f"board_agenda_{date.strftime('%Y_%m_%d')}.txt"

        return self._dir.file(filename)

