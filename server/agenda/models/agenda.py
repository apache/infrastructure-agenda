import os
import functools

from ..utils import svn
from ..parsers import agenda_parser


@functools.total_ordering
class Agenda:
    """A class for Agenda objects

    Attributes:
        date (datetime.date): a date object representing the meeting date
        revision (str): the svn revision of the file this agenda's data came from
        revision_author (str): the last author of this file, based on svn info
        revision_date (datetime.date): a date object of the last svn revision
    """

    def __init__(self, filename):
        self.file = svn.File(filename)
        self.revision = self.file.last_changed_rev
        self.revision_author = self.file.last_changed_author
        self.revision_date = self.file.last_changed_date

        self._parsed_file = agenda_parser.AgendaParser(self.file.path)
        self.date = self._parsed_file.date

    def __repr__(self):
        return f"<Agenda: {self.date}>"

    def __eq__(self, other):
        return self.date == other.date

    def __ne__(self, other):
        return not (self.date == other.date)

    def __lt__(self, other):
        return self.date < other.date


class AgendaList:
    """"""

    def __init__(self):
        pass



# import os
# import datetime
#
# #import flask
#
# from agenda.utils import svn
#
#
# class Agenda(object):
#
#     def __init__(self, data_dir):
#         self._dir = svn.Dir(os.path.join(data_dir, 'repos', 'foundation_board'),
#                             filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
#                             recurse=True)
#
#     def get_all(self, sort=True, desc=False):
#         agendas = self._dir.files
#         # # TODO: this only works the first time the agendas index page is displayed
#         # #       because it changes the underlying objects. So check before changing
#         # #       or do this differently.
#         # for agenda in agendas:
#         #     dt = self._parse_date_from_name(agenda.filename)
#         #     agenda.name = dt.strftime("%a, %d %b %Y")
#         #     agenda.url = flask.url_for('find_agenda', meeting_date=dt)
#         #     agenda.last_changed_date = agenda.last_changed_date.strftime("%c")
#         #     agenda.minutes = self._minutes_filename(agenda.filename)
#         #     agenda.minutes_url = flask.url_for('find_minutes', meeting_date=dt)
#
#         if sort:
#             agendas.sort(reverse=desc)
#
#         return agendas
#
#     def get_by_date(self, date):
#         filename = f"board_agenda_{date.strftime('%Y_%m_%d')}.txt"
#
#         return self._dir.file(filename)
#
#     # TODO: move these to shared module so that we can import into other models
#     @staticmethod
#     def _parse_date_from_name(fname):
#         fname_cleaned = fname.rstrip(".txt").split("_")[2:]
#         return datetime.date(*[int(element) for element in fname_cleaned])
#
#     @staticmethod
#     def _minutes_filename(fname):
#         return fname.replace('board_agenda', 'board_minutes')
#
