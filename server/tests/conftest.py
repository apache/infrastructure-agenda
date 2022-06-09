import os
import subprocess

import pytest

import agenda

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data')


@pytest.fixture
def app():
    app = agenda.init_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def pytest_configure():
    print("Setting up local SVN repo")
    subprocess.run(["svnadmin", "create", f"{DATA_DIR}/tmp"])
    subprocess.run(["svn", "import", f"{DATA_DIR}/repos",
                    f"file:///{DATA_DIR}/tmp/trunk", "-m", "'Initial commit'"])
    subprocess.run(["svn", "checkout", f"file:///{DATA_DIR}/tmp/trunk",
                    f"{DATA_DIR}/repos/"])


def pytest_unconfigure():
    print("Removing local SVN repo")
    subprocess.run(["rm", "-rf", f"{DATA_DIR}/tmp"])
    subprocess.run(["rm", "-rf", f"{DATA_DIR}/repos/.svn"])
