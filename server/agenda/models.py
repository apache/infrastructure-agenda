import os
import re

import flask


class FileModel(object):
    """A parent class for models which are backed by files"""

    # this should pull from the app.config eventually
    _base_dir = os.environ['DATA_DIR']
    _file_regex = r'.*\.txt'
    _data_dir = _base_dir

    def __init__(self):
        pass

    @classmethod
    def _iter_files(cls):
        for dir_, dirs, files in os.walk(cls._data_dir):
            for file in files:
                yield file

    @classmethod
    def get_files(cls):
        file_list = [file
                     for file
                     in cls._iter_files()
                     if re.search(cls._file_regex, str(file))]

        return file_list

    @classmethod
    def get_file(cls, date):
        pass


class Agenda(FileModel):
    """A class for agendas"""
    _file_regex = r'board_agenda_\d{4}_\d{2}_\d{2}\.txt'
    _data_dir = os.path.join(FileModel._base_dir, 'repos/private/foundation/board')

    def __init__(self):
        super().__init__(self)
        pass

class Minutes(FileModel):
    """A class for meeting minutes"""
    _file_regex = r'board_minutes_\d{4}_\d{2}_\d{2}\.txt'
    _data_dir = os.path.join(FileModel._base_dir,
                             'repos/asf/infrastructure/site/trunk/content/foundation/records/minutes')

    def __init__(self):
        super().__init__(self)
        pass
