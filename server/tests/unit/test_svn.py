import os
import datetime

from agenda.utils import svn
import config

CFG = config.TestingConfig
SVN_DIR = svn.Dir(os.path.join(CFG.DATA_DIR,
                               'repos',
                               'foundation_board'),
                  filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                  recurse=True)
SVN_DIR2 = svn.Dir(os.path.join(CFG.DATA_DIR,
                                'repos',
                                'minutes'))
SVN_FILE = SVN_DIR.file('board_agenda_2015_01_21.txt')


def test_dir():
    assert SVN_DIR.path == os.path.join(CFG.DATA_DIR, 'repos', 'foundation_board')
    assert SVN_DIR.last_changed_rev == '1'
    assert SVN_DIR.last_changed_date.date() == datetime.date.today()
    assert len(SVN_DIR) == 2
    assert str(SVN_DIR) == f"<SVNDir: {SVN_DIR.path}>"


def test_file():
    assert SVN_FILE.checksum == '74dc12856a54e292025747ec35052b4a84f04291'
    with open(SVN_FILE.path, 'r') as fp:
        assert SVN_FILE.contents == fp.read()
    assert str(SVN_FILE) == '<SVNFile: board_agenda_2015_01_21.txt>'
