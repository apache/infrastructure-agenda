def test_404(client):
    response = client.get('/api/v1/non_existent_url')

    assert response.status_code == 404
    json_response = response.get_json()
    assert 'not found' in json_response['error']


def test_agendas(client):
    response = client.get("/api/v1/agendas")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 2
    assert json_response['items'][0]['checksum'] == "9925530f37dbbd995e939d72927befd711e9461b"


def test_minutes(client):
    response = client.get("/api/v1/minutes")

    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['count'] == 1
    assert json_response['items'][0]['checksum'] == "881742f842416afa9b9acfb90e31ab214fa54f05"
