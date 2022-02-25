import datetime
import os

import flask

from . import svn


class Agenda(object):

    _dir = svn.Dir(os.path.join(flask.current_app.config['DATA_DIR'], 'repos', 'foundation_board'),
                   filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                   recurse=True)

    def __init__(self):
        pass

    def get_all_agendas(self):

        return [{'filename': agenda.name,
                 'checksum': agenda['checksum'],
                 'revision': agenda['last_changed_rev']}
                for agenda
                in self._dir.files]

    def get_agenda_by_date(self, date):
        filename = f"board_agenda_{date.strftime('%Y_%m_%d')}.txt"

        return self._dir.file(filename)


class Minutes(object):

    _dir = svn.Dir(os.path.join(flask.current_app.config['DATA_DIR'], 'repos', 'minutes'),
                   filter=r'board_minutes_\d{4}_\d{2}_\d{2}\.txt',
                   recurse=True)

    def __init__(self):
        pass

    def get_all_minutes(self):
        
        return [{'filename': minutes.name,
                 'checksum': minutes['checksum'],
                 'revision': minutes['last_changed_rev']}
                for minutes
                in self._dir.files]

    def get_minutes_by_date(self, date):
        filename = f"board_minutes_{date.strftime('%Y_%m_%d')}.txt"

        return self._dir.file(filename)
