import os
import datetime

import pytest

from agenda.utils import svn


def test_dir(config):
    svndir = svn.Dir(os.path.join(config.DATA_DIR, 'repos', 'foundation_board'),
                      filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                      recurse=True)
    assert svndir.path == os.path.join(config.DATA_DIR, 'repos', 'foundation_board')
    assert svndir.last_changed_rev == '1'
    assert svndir.last_changed_date.date() == datetime.date.today()
    assert len(svndir) == 2
    assert str(svndir) == f"<SVNDir: {svndir.path}>"


def test_dir_with_defaults(config):
    svn.Dir(os.path.join(config.DATA_DIR, 'repos', 'minutes'))


def test_file(config):
    svndir = svn.Dir(os.path.join(config.DATA_DIR, 'repos', 'foundation_board'),
                  filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                  recurse=True)
    svn_file = svndir.file('board_agenda_2015_01_21.txt')
    assert svn_file.checksum == '74dc12856a54e292025747ec35052b4a84f04291'
    with open(svn_file.path, 'r') as fp:
        assert svn_file.contents == fp.read()
    assert str(svn_file) == '<SVNFile: board_agenda_2015_01_21.txt>'


def test_file_missing(config):
    svndir = svn.Dir(os.path.join(config.DATA_DIR, 'repos', 'foundation_board'),
                  filter=r'board_agenda_\d{4}_\d{2}_\d{2}\.txt',
                  recurse=True)
    with pytest.raises(FileNotFoundError):
        svndir.file('this_file_is_not_here.txt')
