import subprocess
import os


DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data')


def setup_svn_repo():
    print("Setting up local SVN repo")
    subprocess.run(["svnadmin", "create", f"{DATA_DIR}/tmp"])
    subprocess.run(["svn", "import", f"{DATA_DIR}/repos",
                    f"file:///{DATA_DIR}/tmp/trunk", "-m", "'Initial commit'"])
    subprocess.run(["svn", "checkout", f"file:///{DATA_DIR}/tmp/trunk",
                    f"{DATA_DIR}/repos/"])


def teardown_svn_repo():
    print("Removing local SVN repo")
    subprocess.run(["rm", "-rf", f"{DATA_DIR}/tmp"])
    subprocess.run(["rm", "-rf", f"{DATA_DIR}/repos/.svn"])
