import unittest

import requests

from helpers import endpoint


class TestAccessibility(unittest.TestCase):

    def test_is_accessible(self):
        r = requests.get(endpoint())
        self.assertEqual(r.status_code, 400)

