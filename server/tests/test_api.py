import datetime

import pytest


# general api tests
def test_404(client):
    response = client.get('/api/v1/non_existent_url')

    assert response.status_code == 404
    json_response = response.get_json()
    assert 'not found' in json_response['error']


# agenda endpoint
def test_get_all_agendas(client):
    response = client.get("/api/v1/agendas")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 2
    assert json_response['items'][0]['checksum'] == "74dc12856a54e292025747ec35052b4a84f04291"


def test_get_agenda_by_date(client):
    response = client.get("/api/v1/agendas/2015_02_18")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1


# minutes endpoint
def test_get_all_minutes(client):
    response = client.get("/api/v1/minutes")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1
    assert json_response['items'][0]['checksum'] == "881742f842416afa9b9acfb90e31ab214fa54f05"


def test_get_minutes_by_date(client):
    response = client.get("/api/v1/minutes/2015_01_21")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1


# calendar endpoint
def test_get_all_meetings(client):
    response = client.get("/api/v1/meetings")

    assert response.status_code == 200


@pytest.mark.freeze_time('2015-04-22')
def test_get_next_meeting(client):
    response = client.get("/api/v1/meetings/next")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1
    assert json_response['items'][0] == 'Wed, 20 May 2015 22:00:00 GMT'


@pytest.mark.freeze_time('2015-04-22')
def test_get_prev_meeting(client):
    response = client.get("/api/v1/meetings/prev")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1
    assert json_response['items'][0] == 'Wed, 15 Apr 2015 22:00:00 GMT'


def test_get_meeting_by_month(client):
    response = client.get("/api/v1/meetings/2015/06")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1
    assert json_response['items'][0] == 'Wed, 17 Jun 2015 22:00:00 GMT'


# committee endpoint
def test_get_all_committees(client):
    response = client.get("/api/v1/committees")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 19
    assert json_response['items'][0]['name'] == 'arbustum'


def test_get_committee_by_name(client):
    response = client.get("/api/v1/committees/pteric")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1
    assert json_response['items'][0]['name'] == 'pteric'

# get committees by reporting month
# get committees reporting next meeting
