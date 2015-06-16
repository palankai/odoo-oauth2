import unittest

import requests

from helpers import endpoint


class TestAccessibility(unittest.TestCase):

    def test_is_accessible(self):
        r = requests.get(endpoint())
        self.assertEqual(r.status_code, 400)

    def test_get_request(self):
        r = requests.get(endpoint(), {"grant_type": "refresh_token"})
        self.assertEqual(r.status_code, 400)

    def test_post_request(self):
        r = requests.post(endpoint(), {"grant_type": "refresh_token"})
        self.assertEqual(r.status_code, 200)

    def test_headers_request(self):
        r = requests.post(
            endpoint(),
            {"grant_type": "password"},
            headers={"Authorization": "123"}
        )
        self.assertEqual(r.status_code, 200)

