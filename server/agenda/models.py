import os
import re
import datetime

import flask


class FileModel(object):
    """A parent class for models which are backed by files"""

    # this should pull from the app.config eventually
    _base_dir = os.environ['DATA_DIR']
    _file_regex = r'.*\.txt'
    _data_dir = _base_dir

    def __init__(self):
        self._items = self._add_files()

    def _add_files(self):
        file_list = [{"file": file, "date": self._parse_date(file)}
                     for file
                     in self._iter_files()
                     if re.search(self._file_regex, str(file))]

        return file_list

    @classmethod
    def _iter_files(cls):
        for dir_, dirs, files in os.walk(cls._data_dir):
            for file in files:
                yield file

    @staticmethod
    def _parse_date(filename):
        date_str = filename[:-4].split('_', 2)[2]
        parse_date = datetime.datetime.strptime(date_str, '%Y_%m_%d').date()
        
        return parse_date

    def get_items(self, sort=True):
        items = self._items
        if sort is True:
            return sorted(items, key=lambda x: x['date'])
        else: 
            return items

    @classmethod
    def get_file(cls, date):
        pass


class Agenda(FileModel):
    """A class for agendas"""
    _file_regex = r'board_agenda_\d{4}_\d{2}_\d{2}\.txt'
    _data_dir = os.path.join(FileModel._base_dir, 
                             'repos/private/foundation/board')

    def __init__(self):
        super().__init__()
        pass

class Minutes(FileModel):
    """A class for meeting minutes"""
    _file_regex = r'board_minutes_\d{4}_\d{2}_\d{2}\.txt'
    _data_dir = os.path.join(FileModel._base_dir,
                             'repos/asf/infrastructure/site/trunk/content/foundation/records/minutes')

    def __init__(self):
        super().__init__()
        pass
