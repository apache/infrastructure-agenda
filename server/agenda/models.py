import datetime
import os

from . import svn


class Agenda(object):

    _dir = svn.Dir(os.path.join(os.environ['DATA_DIR'], 'repos/private/foundation/board'),
                   filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                   recurse=True)

    def __init__(self):
        pass

    def get_agendas(self):
        
        return [{'filename': agenda.name,
                 'checksum': agenda.info['checksum'],
                 'revision': agenda.info['last_changed_rev']}
                for agenda
                in self._dir.files]


class Minutes(object):

    _dir = svn.Dir(os.path.join(os.environ['DATA_DIR'], 'repos/asf/infrastructure/site/trunk/content/foundation/records/minutes'),
                   filter=r'board_minutes_\d{4}_\d{2}_\d{2}\.txt',
                   recurse=True)

    def __init__(self):
        pass

    def get_minutes(self):
        
        return [{'filename': minutes.name,
                 'checksum': minutes.info['checksum'],
                 'revision': minutes.info['last_changed_rev']}
                for minutes
                in self._dir.files]