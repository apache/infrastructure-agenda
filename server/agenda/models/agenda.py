import os
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
        self.parsed_file = agenda_parser.AgendaParser(self.file.path)

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
    SKIP_LIST = ['board_agenda_2008_01_16.txt', # TODO: put this list in a puppet stored file and load it here
                 'board_agenda_2011_11_07.txt',
                 'board_agenda_2010_09_11.txt',
                 'board_agenda_2010_10_20.txt',
                 'board_agenda_2006_08_16.txt',
                 'board_agenda_2011_03_16.txt',
                 'board_agenda_2005_11_16.txt',
                 'board_agenda_2006_01_18.txt',
                 'board_agenda_2012_08_28.txt',
                 'board_agenda_2005_10_26.txt',
                 'board_agenda_2006_05_24.txt',
                 'board_agenda_2005_12_21.txt',
                 'board_agenda_2005_07_28.txt',
                 'board_agenda_2010_03_17.txt',
                 'board_agenda_2010_11_17.txt',
                 'board_agenda_2010_11_02.txt',
                 'board_agenda_2006_02_15.txt',
                 'board_agenda_2009_11_01.txt',
                 'board_agenda_2006_09_20.txt',
                 'board_agenda_2007_08_29.txt',
                 'board_agenda_2019_05_16.txt',
                 'board_agenda_2007_04_25.txt',
                 'board_agenda_2010_01_20.txt',
                 'board_agenda_2009_11_18.txt',
                 'board_agenda_2011_05_19.txt',
                 'board_agenda_2006_12_20.txt',
                 'board_agenda_2006_10_25.txt',
                 'board_agenda_2011_02_16.txt',
                 'board_agenda_2007_03_28.txt',
                 'board_agenda_2007_11_14.txt',
                 'board_agenda_2006_04_26.txt',
                 'board_agenda_2009_12_16.txt',
                 'board_agenda_2010_12_15.txt',
                 'board_agenda_2008_03_19.txt',
                 'board_agenda_2011_08_17.txt',
                 'board_agenda_2017_06_15.txt',
                 'board_agenda_2006_06_27.txt',
                 'board_agenda_2006_03_15.txt',
                 'board_agenda_2010_02_17.txt',
                 'board_agenda_2011_01_19.txt',
                 'board_agenda_2010_09_22.txt']

    def __init__(self, directory):
        self._files = [ ]
        # TODO: update the pattern after utf-8 encoding issues figured out on old agendas
        for path in pathlib.Path(os.path.join(directory, 'foundation_board')).rglob(r'board_agenda_????_??_??.txt'):
            if path.name not in self.SKIP_LIST:
                self._files.append(path)

        self.agendas = [ ]
        # cnt = 0
        for f in self._files:
            # cnt += 1
            # print(f"{cnt}: {f.name}")
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
