import datetime
import os
import re

import flask

from . import svn
from . import parseci


class Agenda(object):

    _dir = svn.Dir(os.path.join(flask.current_app.config['DATA_DIR'], 'repos', 'foundation_board'),
                   filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                   recurse=True)

    def __init__(self):
        pass

    def get_all(self):

        return [{'filename': agenda.name,
                 'checksum': agenda['checksum'],
                 'revision': agenda['last_changed_rev']}
                for agenda
                in self._dir.files]

    def get_by_date(self, date):
        filename = f"board_agenda_{date.strftime('%Y_%m_%d')}.txt"

        return self._dir.file(filename)


class Minutes(object):

    _dir = svn.Dir(os.path.join(flask.current_app.config['DATA_DIR'], 'repos', 'minutes'),
                   filter=r'board_minutes_\d{4}_\d{2}_\d{2}\.txt',
                   recurse=True)

    def __init__(self):
        pass

    def get_all(self):
        
        return [{'filename': minutes.name,
                 'checksum': minutes['checksum'],
                 'revision': minutes['last_changed_rev']}
                for minutes
                in self._dir.files]

    def get_by_date(self, date):
        filename = f"board_minutes_{date.strftime('%Y_%m_%d')}.txt"

        return self._dir.file(filename)


class Meeting(object):

    _cal_file = os.path.join(flask.current_app.config['DATA_DIR'], 
                             'repos', 
                             'committers_board',
                             'calendar.txt')

    def __init__(self):
        with open(self._cal_file, "r") as f:
            matches = re.findall(r'^\s+\*\)\s(.*)$', f.read(), re.MULTILINE)

            self._dates = [datetime.datetime.strptime(match, "%a, %d %B %Y, %H:%M %Z")
                           for match
                           in matches]

    def get_all(self):
        return self._dates

    def get_next(self):
        future_meetings = [mtg
                           for mtg
                           in self._dates
                           if mtg >= datetime.datetime.now()]

        return [future_meetings[0]]

    def get_prev(self):
        past_meetings = [mtg
                         for mtg
                         in self._dates[-1::-1]
                         if mtg <= datetime.datetime.now()]

        return [past_meetings[0]]

    def get_by_month(self, year, month):
        meetings = [mtg
                    for mtg
                    in self._dates
                    if mtg.month == month and mtg.year == year]

        return [meetings[0]]


class Committee(object):
    
    _data_file = os.path.join(flask.current_app.config['DATA_DIR'],
                              'repos',
                              'committers_board',
                              'committee-info.txt')

    def __init__(self):
        with open(self._data_file, 'r') as fp:
            self._data = parseci.parse_info(fp)

    def get_all(self):
        return self._data

    def get_by_name(self, name):
        committees = [committee
                      for committee
                      in self._data
                      if committee['name'] == name]

        return [committees[0]]
