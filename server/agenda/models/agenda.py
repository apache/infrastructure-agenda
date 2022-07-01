import os
import functools
import pathlib

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
        self.rev_date_str = self.revision_date.strftime("%c")

        self._parsed_file = agenda_parser.AgendaParser(self.file.path)
        self.date = self._parsed_file.date
        self.url = '#'
        self.name = self.date.strftime("%a, %d %b %Y")
        self.roll_call = self._parsed_file.roll_call

    def __repr__(self):
        return f"<Agenda: {self.date}>"

    def __eq__(self, other):
        return self.date == other.date

    def __ne__(self, other):
        return not (self.date == other.date)

    def __lt__(self, other):
        return self.date < other.date


class AgendaList:
    """A class for lists of Agenda objects

    """

    def __init__(self, directory):
        self._files = [ ]
        # TODO: update the pattern after utf-8 encoding issues figured out on old agendas
        for path in pathlib.Path(os.path.join(directory, 'foundation_board')).rglob(r'board_agenda_??21_??_??.txt'):
            self._files.append(path)

        self.agendas = [ ]
        for f in self._files:
            self.agendas.append(Agenda(f))

    def __len__(self):
        return len(self._files)

    def get_by_date(self, date):
        results = [agenda for agenda in self.agendas if agenda.date == date]

        return results[0]

    def get_all(self):
        return self.agendas
