import subprocess
import re
import os


class FSObject(object):
    """A parent class for the following two classes
    """

    def __init__(self, path, *args, **kwargs):
        self._path = path
        self._info = self._get_info()

    @property
    def path(self):
        return self._path

    @property
    def info(self):
        return self._info

    def _get_info(self):
        try:
            output = subprocess.run(["svn", "info", self._path],
                                    check=True,
                                    text=True, 
                                    capture_output=True)
        except subprocess.CalledProcessError:
            raise NotSVNRepoError

        info = {}
        clean_output = output.stdout.strip()
        for line in clean_output.split('\n'):
            k, v = line.split(':', 1)
            info[k.replace(" ", "_").lower()] = v.strip()

        return info

    def __getitem__(self, item):
        return self._info[item]


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

        self._files = self._walkdir()

    @property
    def files(self):
        return self._files

    def file(self, filename):
        """return a File object

            Arguments:
                filename: name of the file being requested
        """
        for f in self.files:
            if f.name == filename:
                return f
        raise FileNotFoundError

    def update(self):
        """update the directory

            Returns: the output of the `svn up` command
        """
        try:
            output = subprocess.run(["svn", "up", self._path],
                                    check=True,
                                    text=True,
                                    capture_output=True)
        except subprocess.CalledProcessError:
            raise NotSVNRepoError

        return output


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
            return file.read()
    
    def __repr__(self):
        return f"<SVNFile: {self.name}>"


class NotSVNRepoError(Exception):
    """Raised when a filesystem object doesn't pertain to an SVN repository"""
    pass
