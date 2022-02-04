import datetime
import subprocess
import re


class Repo(object):
    """A class containing access to ASF SVN repositories

    Attributes:
        last_update: timestamp of when the working
          directory was last updated
        url: url of the remote repo
        workdir: path of the local workdir
        uuid: remote repo root uuid
        revision: current revision in workdir
    """

    _repo_base = 'https://svn.apache.org/repos'
    _work_base = '../data'

    def __init__(self, path, directory):
        """Inits Repo

        Args:
            path: target path of remote repo
            directory: path of local workdir
        """
        self._url = f"{self._repo_base}/{path}"
        self._workdir = f"{self._work_base}/{directory}"
        self._uuid = None
        self._revision = None

        self.update_content()

    @property
    def last_update(self):
        return self._last_update

    @property
    def url(self):
        return self._url

    @property
    def workdir(self):
        return self._directory

    @property
    def uuid(self):
        return self._uuid

    @property
    def revision(self):
        return self._revision
    
    def _update_meta(self, info):
        """This function updates the repo metadata"""
        self._uuid, self._revision = self._parse_svninfo(info)
        self._last_update = datetime.datetime.now()

    @staticmethod
    def _parse_svninfo(info):
        """This function parses out a few useful bits and updates class vars"""
        uuid_match = re.search(r'^Repository\ UUID: (.*)$', info, re.MULTILINE)
        revision_match = re.search(r'^Revision: (.*)$', info, re.MULTILINE)
        
        return [uuid_match[1], revision_match[1]]

    def update_content(self):
        """This function updates the local repo content"""
        results = None
        try:
            results = subprocess.run(["svn", "info", self._directory], 
                                     check=True, 
                                     text=True, 
                                     capture_output=True)
        except subprocess.CalledProcessError:
            subprocess.run(["svn", "checkout", self._url, self._directory])
        else:
            subprocess.run(["svn", "up", self._directory])
        finally:
            self._update_meta(results.stdout)
