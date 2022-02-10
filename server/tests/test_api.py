import unittest
import json

import agenda


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = agenda.create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_404(self):
        response = self.client.get(
            '/api/v1/wrong_url_etc')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'not found')

    def test_agendas(self):
        response = self.client.get(
            '/api/v1/agendas')

        self.assertEqual(response.status_code, 200)

    def test_minutes(self):
        response = self.client.get(
            '/api/v1/minutes')

        self.assertEqual(response.status_code, 200)
