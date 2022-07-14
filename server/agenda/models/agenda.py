import functools
import pathlib
import datetime

from ..utils import svn
from ..parsers import agenda_parser


@functools.total_ordering
class Agenda:
    """A class for Agenda objects

    Attributes:
        file (SVNFile): An SVNFile object pointing to the local file on disk
        date (datetime.date): a date object representing the meeting date
        name (str): the name of the Agenda (string representation of the meeting date)
        parsed_file (AgendaParser): A parsed version of the agenda text file
    """

    def __init__(self, filename):
        self.file = svn.File(filename)
        self.date = self._get_date_from_filename(self.file.path)
        self.name = self.date.strftime("%a, %d %b %Y")
        try:
            self.parsed_file = agenda_parser.AgendaParser(self.file.path)
        except AttributeError:
            self.parsed_file = None

    def __repr__(self):
        return f"<Agenda: {self.date}>"

    def __eq__(self, other):
        return self.date == other.date

    def __ne__(self, other):
        return not (self.date == other.date)

    def __lt__(self, other):
        return self.date < other.date

    @staticmethod
    def _get_date_from_filename(filename):
        d = pathlib.Path(filename).stem.split('_')
        date_bits = [int(item) for item in d[2:5]]
        return datetime.date(*date_bits)


class AgendaList:
    """A class for lists of Agenda objects

    """

    def __init__(self, repo_dir):
        self._files = [ ]
        for path in pathlib.Path(repo_dir).rglob(r'board_agenda_????_??_??.txt'):
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

    def refresh_by_date(self, date):
        a = self.get_by_date(date)

        file_path = a.file.path
        self.agendas.remove(a)
        self.agendas.append(Agenda(file_path))
