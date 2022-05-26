import os

import flask

from server.agenda.utils import svn

class Minutes(object):

    def __init__(self):
        self._dir = svn.Dir(os.path.join(flask.current_app.config['DATA_DIR'],
                                         'repos',
                                         'minutes'),
                            filter=r'board_minutes_\d{4}_\d{2}_\d{2}\.txt',
                            recurse=True)

    def get_all(self):
        return [{'filename': minutes.name,
                 'checksum': minutes['checksum'],
                 'revision': minutes['last_changed_rev']}
                for minutes
                in self._dir.files]

    def get_by_date(self, date):
        filename = f"board_minutes_{date.strftime('%Y_%m_%d')}.txt"

        return self._dir.file(filename)
