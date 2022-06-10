import subprocess
import re
import os
import datetime
from functools import total_ordering



class FSObject(object):
    """A parent class for the following two classes
    """

    DATETIME_PATTERN="%Y-%m-%d %H:%M:%S %z"

    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.info = self._get_info()
        self.last_changed_author = self.info['last_changed_author']
        self.last_changed_rev = self.info['last_changed_rev']
        self.last_changed_date = datetime.datetime.strptime(self.info['last_changed_date'].split(' (')[0],
                                                            self.DATETIME_PATTERN)

    def _get_info(self):
        output = subprocess.run(["svn", "info", self.path],
                                    check=True,
                                    text=True, 
                                    capture_output=True)

        info = {}
        clean_output = output.stdout.strip()
        for line in clean_output.split('\n'):
            k, v = line.split(':', 1)
            info[k.replace(" ", "_").lower()] = v.strip()

        return info

    # def __getitem__(self, item):
    #     return self.info[item]


class Dir(FSObject):
    """A class facilitating access to an SVN backed directory
        
        Attributes:
            path: full path to this dir
            info: SVN info for this dir
            files: given an optional filter, the list of files in this dir
              and the nested directories if recursion is specified
    """

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

        self.files = self._walkdir()

    def file(self, filename):
        """return a File object

            Arguments:
                filename: name of the file being requested
        """
        for f in self.files:
            if f.filename == filename:
                return f
        raise FileNotFoundError

    # def update(self):
    #     """update the directory
    #
    #         Returns: the output of the `svn up` command
    #     """
    #     output = subprocess.run(["svn", "up", self.path],
    #                             check=True,
    #                             text=True,
    #                             capture_output=True)
    #
    #     return output


    def _walkdir(self):
        """create a list of files in this dir and return it"""
        if self._recurse:
            file_list = [File(f"{file[0]}/{file[1]}")
                         for file
                         in self._iter_files()
                         if re.search(self._filter, str(file[1]))]
        else:
            file_list = [File(f"{self.path}/{file}")
                         for file
                         in os.listdir(self.path)
                         if re.search(self._filter, str(file))]

        return file_list

    def _iter_files(self):
        """generator method to allow filtering of os.walk()"""
        for dir_, dirs, files in os.walk(self.path):
            for file in files:
                yield (dir_, file)

    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return f"<SVNDir: {self.path}>"


@total_ordering
class File(FSObject):
    """A class facilitating access to an SVN backed directory

        Attributes:
            path: full path to this file
            info: SVN info for this file
            name: filename
            contents: contents of the file

    """

    def __init__(self, path, *args, **kwargs):
        """Inits File object

            Arguments:
                path: full path to this file
        """
        super().__init__(path, *args, **kwargs)
        self.filename = os.path.split(self.path)[1]
        self.checksum = self.info['checksum']

    @property
    def contents(self):
        with open(self.path, 'r') as file:
            return file.read()
    
    def __repr__(self):
        return f"<SVNFile: {self.filename}>"

    def __eq__(self, other):
        return self.filename == other.filename

    def __ne__(self, other):
        return not (self.filename == other.filename)

    def __lt__(self, other):
        return self.filename < other.filename
