import os
import datetime

import pytest

from agenda.utils import svn
import config

CFG = config.TestingConfig
SVN_DIR = svn.Dir(os.path.join(CFG.DATA_DIR, 'repos', 'foundation_board'),
                  filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                  recurse=True)


def test_dir():
    assert SVN_DIR.path == os.path.join(CFG.DATA_DIR, 'repos', 'foundation_board')
    assert SVN_DIR.last_changed_rev == '1'
    assert SVN_DIR.last_changed_date.date() == datetime.date.today()
    assert len(SVN_DIR) == 2
    assert str(SVN_DIR) == f"<SVNDir: {SVN_DIR.path}>"


def test_dir_with_defaults():
    svn.Dir(os.path.join(CFG.DATA_DIR, 'repos', 'minutes'))


def test_file():
    svn_file = SVN_DIR.file('board_agenda_2015_01_21.txt')
    assert svn_file.checksum == '74dc12856a54e292025747ec35052b4a84f04291'
    with open(svn_file.path, 'r') as fp:
        assert svn_file.contents == fp.read()
    assert str(svn_file) == '<SVNFile: board_agenda_2015_01_21.txt>'

def test_file_missing():
    with pytest.raises(FileNotFoundError):
        SVN_DIR.file('this_file_is_not_here.txt')
