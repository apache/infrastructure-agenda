import os

import flask

from agenda.parsers import parseci

class Committee(object):

    def __init__(self):
        self._data_file = os.path.join(flask.current_app.config['DATA_DIR'],
                                       'repos',
                                       'committers_board',
                                       'committee-info.txt')

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
