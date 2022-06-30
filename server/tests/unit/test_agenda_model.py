import os
import datetime

from agenda.models import agenda


def test_agenda_attributes(config):
    a = agenda.Agenda(os.path.join(config.DATA_DIR, 'repos', 'foundation_board', 'board_agenda_2015_02_18.txt'))

    assert a.revision == '1'
    assert a.revision_author == os.getenv('USER')
    assert a.revision_date.date() == datetime.date.today()
    assert a.date == datetime.date(2015, 2, 18)


def test_agenda_magic(config):
    a = agenda.Agenda(os.path.join(config.DATA_DIR, 'repos', 'foundation_board', 'board_agenda_2015_01_21.txt'))
    b = agenda.Agenda(os.path.join(config.DATA_DIR, 'repos', 'foundation_board', 'board_agenda_2015_02_18.txt'))

    assert a.__repr__() == '<Agenda: 2015-01-21>'
    assert a < b
    assert a == a
    assert a != b



def test_agenda_sorting(config):
    a = agenda.Agenda(os.path.join(config.DATA_DIR, 'repos', 'foundation_board', 'board_agenda_2015_01_21.txt'))
    b = agenda.Agenda(os.path.join(config.DATA_DIR, 'repos', 'foundation_board', 'board_agenda_2015_02_18.txt'))

    tmp_list = [a, b]
    tmp_list.sort(reverse=True)

    assert tmp_list[0].date == datetime.date(2015, 2, 18)


def test_agenda_list(config):
    agenda_list = agenda.AgendaList(os.path.join(config.DATA_DIR, 'repos', 'foundation_board'))
    assert len(agenda_list) == 2

    a = agenda_list.get_by_date(datetime.date(2015, 2, 18))
    assert a.date == datetime.date(2015, 2, 18)

    aa = agenda_list.get_all()
    assert len(aa) == 2