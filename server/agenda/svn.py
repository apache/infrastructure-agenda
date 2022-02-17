import subprocess
import re
import os


class FSObject(object):
    """A parent class for the following two classes
    """

    def __init__(self, path, *args, **kwargs):
        self._path = path
        self._info_regex = r''

    @property
    def path(self):
        return self._path

    @property
    def info(self):
        results = self._svninfo()
        info = re.search(self._info_regex, results.stdout, re.MULTILINE)

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


class Dir(FSObject):
    """A class facilitating access to an SVN backed directory

    """

    def __init__(self, path, *args, **kwargs):
        """Inits directory object
        """
        super().__init__(path, *args, **kwargs)
        self._info_regex = r'''^Path:\s(?P<path>.*)$
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
^Last\sChanged\sDate:\s(?P<last_changed_date>.*)$'''
        
        if 'filter' in kwargs:
            self._filter = kwargs['filter']
        else:
            self._filter = r'.*'
        if 'recurse' in kwargs:
            self._recurse = kwargs['recurse']
        else:
            self._recurse = False

    @property
    def files(self):
        return self._walkdir()

    def file(self, file):
        if file in self.files:
            return file

    def _walkdir(self):
        if self._recurse:
            file_list = [file
                         for file
                         in self._iter_files()
                         if re.search(self._filter, str(file))]
        else:
            file_list = [File(f"{self._path}/{file}")
                         for file
                         in os.listdir(self._path) 
                         if re.search(self._filter, str(file))]

        return file_list

    def _iter_files(self):
        for dir_, dirs, files in os.walk(self._path):
            for file in files:
                yield file


    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return f"<SVNDir: {self.path}>"


class File(FSObject):
    """A class facilitating access to an SVN backed directory
    """

    def __init__(self, path, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self._info_regex = r'''^Path:\s(?P<path>.*)$
^Name:\s(?P<name>.*)$
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
^Last\sChanged\sDate:\s(?P<last_changed_date>.*)$
^Text\sLast\sUpdated:\s(?P<text_last_updated>.*)$
^Checksum:\s(?P<checksum>.*)$'''

    @property
    def name(self):
        return os.path.split(self._path)[1]

    @property
    def contents(self):
        with open(self._path, 'r')as file:
            return file.readlines()
    
    def __repr__(self):
        return f"<SVNFile: {self.name}>"


class NotSVNRepoError(Exception):
    """Raised when a filesystem object doesn't pertain to an SVN repository"""
    pass
