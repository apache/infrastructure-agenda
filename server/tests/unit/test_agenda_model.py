from agenda.models import agenda


def test_get_all(config):
    agendas = agenda.Agenda(config.DATA_DIR).get_all()

    assert len(agendas) == 2

def test_get_all_sorted(config):
    agendas = agenda.Agenda(config.DATA_DIR).get_all(sort=True, order="desc")

    assert agendas[0].filename == 'board_agenda_2015_02_18.txt'
