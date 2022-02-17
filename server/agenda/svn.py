import subprocess
import re
import os


class FSObject(object):
    """A parent class for the following two classes
    """

    _info_regex = r''

    def __init__(self, path, *args, **kwargs):
        self._path = path

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
        
        Attributes:
            path: full path to this dir
            info: SVN info for this dir
            files: given an optional filter, the list of files in this dir
              and the nested directories if recursion is specified
    """

    _info_regex = r'''^Path:\s(?P<path>.*)$
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

    def __init__(self, path, *args, **kwargs):
        """Inits directory object

            Arguments:
                path: full path to this dir (required)
                filter: regex pattern with which to filter files
                recurse: boolean argument to enable directory recursion
        """
        super().__init__(path, *args, **kwargs)
                
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

    def _walkdir(self):
        """create a list of files in this dir and return it"""
        if self._recurse:
            file_list = [File(f"{file[0]}/{file[1]}")
                         for file
                         in self._iter_files()
                         if re.search(self._filter, str(file[1]))]
        else:
            file_list = [File(f"{self._path}/{file}")
                         for file
                         in os.listdir(self._path) 
                         if re.search(self._filter, str(file))]

        return file_list

    def _iter_files(self):
        """generator method to allow filtering of os.walk()"""
        for dir_, dirs, files in os.walk(self._path):
            for file in files:
                yield (dir_, file)

    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return f"<SVNDir: {self.path}>"


class File(FSObject):
    """A class facilitating access to an SVN backed directory

        Attributes:
            path: full path to this file
            info: SVN info for this file
            name: filename
            contents: contents of the file

    """

    _info_regex = r'''^Path:\s(?P<path>.*)$
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

    def __init__(self, path, *args, **kwargs):
        """Inits File object

            Arguments:
                path: full path to this file
        """
        super().__init__(path, *args, **kwargs)
        
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
