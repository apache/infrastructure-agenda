def test_404(client):
    response = client.get('/api/v1/non_existent_url')

    assert response.status_code == 404
    json_response = response.get_json()
    assert 'not found' in json_response['error']


def test_agendas(client):
    response = client.get("/api/v1/agendas")

    assert response.status_code == 200


def test_minutes(client):
    response = client.get("/api/v1/minutes")

    assert response.status_code == 200
