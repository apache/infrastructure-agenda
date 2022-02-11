def test_404(client):
    response = client.get('/api/v1/non_existent_url')

    assert response.status_code == 404
    json_response = response.get_json()
    assert 'not found' in json_response['error']


def test_agendas(client):
    response = client.get("/api/v1/agendas")

    assert response.status_code == 200
    json_response = response.get_json()
    assert 'board_agenda_2005_07_28.txt' in json_response


def test_minutes(client):
    response = client.get("/api/v1/minutes")

    assert response.status_code == 200
    json_response = response.get_json()
    assert 'board_minutes_1999_04_13.txt' in json_response
