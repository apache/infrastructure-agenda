import subprocess
import re
import os


class Dir(object):
    """A class facilitating access to an SVN backed directory

    """

    def __init__(self, path, *args, **kwargs):
        """Inits directory object
        """
        self._path = path

        # request svn info quickly to ensure we are in an SVN repo
        self._svninfo()
        
        if 'filter' in kwargs:
            self._filter = kwargs['filter']
        else:
            self._filter = r'.*'
        if 'recurse' in kwargs:
            self._recurse = kwargs['recurse']
        else:
            self._recurse = False

    @property
    def path(self):
        return self._path
    
    @property
    def files(self):
        pass

    @property
    def info(self):
        results = self._svninfo()
        info_regex = r'''^Path:\s(?P<path>.*)$
^Working\sCopy\sRoot\sPath:\s(?P<working_copy_root_path>.*)$
^URL:\s(?P<url>.*)$
^Relative\sURL:\s(?P<relative_url>.*)$
^Repository\sRoot:\s(?P<repository_root>.*)$
^Repository\sUUID:\s(?P<repository_uuid>.*)$
^Revision:\s(?P<revision>.*)$
^Node\sKind:\s(?P<node_kind>.*)$
^Schedule:\s(?P<schedule>.*)$
^Last\sChanged\sAuthor:\s(?P<last_changed_author>.*)$
^Last\sChanged\sRev:\s(?P<last_changed_rev>.*)$
Last\sChanged\sDate:\s(?P<last_changed_date>.*)$'''
  
        info = re.search(info_regex, results.stdout, re.MULTILINE)

        return info.groupdict()
    
    def _svninfo(self):
        try:
            results = subprocess.run(["svn", "info", self._path],
                                     check=True,
                                     text=True, 
                                     capture_output=True)
        except subprocess.CalledProcessError:
            raise NotSVNRepoError

        return results

    def _walkdir(self):
        if self._recurse:
            file_list = [file
                         for file
                         in self._iter_files()
                         if re.search(self._filter, str(file))]
        else:
            file_list = [file
                         for file
                         in os.listdir(self._path) 
                         if re.search(self._filter, str(file))]

        return file_list

    def _iter_files(self):
        for dir_, dirs, files in os.walk(self._path):
            for file in files:
                yield file

    def __repr__(self):
        return f"<SVNDir: {self.path}>"


class NotSVNRepoError(Exception):
    """Raised when a filesystem object doesn't pertain to an SVN repository"""
    pass
