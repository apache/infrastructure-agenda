import os
import re

import flask

# this should pull from the app.config eventually
base_dir = '/home/iroh/Projects/asf-agenda/infrastructure-agenda/server/data'


class Agenda(object):
    """A class for agendas"""
    _data_dir = os.path.join(base_dir, 'repos/private/foundation/board')
    _file_regex = r'board_agenda_\d{4}_\d{2}_\d{2}\.txt'

    def __init__(self):
        pass

    @classmethod
    def get_files(cls):
        file_list = [file
                     for file
                     in _iter_files(cls._data_dir)
                     if re.search(cls._file_regex, str(file))]

        return file_list


def _iter_files(directory):
    for dir_, dirs, files in os.walk(directory):
        for file in files:
            yield file
