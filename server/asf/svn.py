import datetime
import subprocess
import re
import os


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

    _work_base = os.environ.get('DATA_DIR')

    def __init__(self, url, depth="infinity"):
        """Inits Repo

        Args:
            url: target url of a remote repo
            depth: desired checkout depth (default=infinity)
        """
        self._url = url
        self._workdir = f"{self._work_base}/{self._parse_path_from_url(url)}"
        self._depth = depth
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
        return self._workdir

    @property
    def depth(self):
        return self._depth
    
    @property
    def uuid(self):
        return self._uuid

    @property
    def revision(self):
        return self._revision
    
    def _update_meta(self, info):
        """Updates the repo metadata
        
        Args:
            info: the output from `svn info <local dir>`
        """
        self._uuid, self._revision = self._parse_svninfo(info)
        self._last_update = datetime.datetime.now()

    @staticmethod
    def _parse_svninfo(info):
        """Parses out a few useful bits and updates class vars"""
        uuid_match = re.search(r'^Repository\ UUID: (.*)$', info, re.MULTILINE)
        revision_match = re.search(r'^Revision: (.*)$', info, re.MULTILINE)
        
        return [uuid_match[1], revision_match[1]]

    @staticmethod
    def _parse_path_from_url(url):
        """Create a path relative path from a given url"""
        split_url = url.split('/')
        repos_idx = split_url.index('repos')

        return os.path.join(*split_url[repos_idx:])

    def update_content(self):
        """Updates local repo content"""
        results = None
        try:
            results = subprocess.run(["svn", "info", self._workdir], 
                                     check=True, 
                                     text=True, 
                                     capture_output=True)
        except subprocess.CalledProcessError:
            subprocess.run(["svn", "checkout", f"--depth={self._depth}", 
                            self._url, self._workdir])

            # this seems like a kludge and should probably be DRY'ed up
            results = subprocess.run(["svn", "info", self._workdir], 
                                     check=True, 
                                     text=True, 
                                     capture_output=True)
        else:
            subprocess.run(["svn", "up", self._workdir])
        finally:
            self._update_meta(results.stdout)
