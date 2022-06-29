import os
import subprocess

import pytest

import agenda
import config

cfg = config.TestingConfig


@pytest.fixture
def app():
    app = agenda.init_app(cfg)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def config():
    return cfg


def pytest_configure():
    print("Setting up local SVN repo")
    subprocess.run(["svnadmin", "create", f"{cfg.DATA_DIR}/tmp"])
    subprocess.run(["svn", "import", f"{cfg.DATA_DIR}/repos",
                    f"file:///{cfg.DATA_DIR}/tmp/trunk", "-m", "'Initial commit'"])
    subprocess.run(["svn", "checkout", f"file:///{cfg.DATA_DIR}/tmp/trunk",
                    f"{cfg.DATA_DIR}/repos/"])


def pytest_unconfigure():
    print("Removing local SVN repo")
    subprocess.run(["rm", "-rf", f"{cfg.DATA_DIR}/tmp"])
    subprocess.run(["rm", "-rf", f"{cfg.DATA_DIR}/repos/.svn"])
