import subprocess

import pytest

import agenda


@pytest.fixture
def app():
    app = agenda.create_app('testing')

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


config = agenda.config['testing']
data_dir = config.DATA_DIR


def pytest_configure():
    print("Setting up local SVN repo")
    subprocess.run(["svnadmin", "create", f"{data_dir}/tmp"])
    subprocess.run(["svn", "import", f"{data_dir}/repos", 
                    f"file:///{data_dir}/tmp/trunk", "-m", "'Initial commit'"])
    subprocess.run(["svn", "checkout", f"file:///{data_dir}/tmp/trunk", 
                    f"{data_dir}/repos/"])


def pytest_unconfigure():
    print("Removing local SVN repo")
    subprocess.run(["rm", "-rf", f"{data_dir}/tmp"])
    subprocess.run(["rm", "-rf", f"{data_dir}/repos/.svn"])
