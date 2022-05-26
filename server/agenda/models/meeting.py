import os
import datetime
import re

import flask

class Meeting(object):

    def __init__(self):

        self._cal_file = os.path.join(flask.current_app.config['DATA_DIR'],
                                      'repos',
                                      'committers_board',
                                      'calendar.txt')

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