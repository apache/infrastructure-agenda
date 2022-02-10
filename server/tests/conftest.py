import pytest

import agenda


@pytest.fixture
def app():
    app = agenda.create_app('testing')

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
