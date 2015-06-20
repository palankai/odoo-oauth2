import base64
import unittest
import time

import requests

from helpers import endpoint, call


class TestAccessibility(unittest.TestCase):

    def DONOT_test_is_accessible(self):
        r = requests.get(endpoint())
        self.assertEqual(r.status_code, 400)

    def DONOT_test_get_request(self):
        r = requests.get(endpoint(), {"grant_type": "refresh_token"})
        self.assertEqual(r.status_code, 400)

    def DONOT_test_post_request(self):
        r = requests.post(endpoint(), {"grant_type": "refresh_token"})
        self.assertEqual(r.status_code, 200)


class TestLoginWithClientAuth(unittest.TestCase):

    def test_login(self):
        k,s = self.create_client()
        r = requests.post(
            endpoint(), 
            {
                "grant_type": "password",
                "username":"admin",
                "password": "admin"
            }, headers={
                "Authorization":"basic %s" % base64.b64encode("%s:%s" % (k,s))
            })
        self.assertEqual(r.status_code, 200)

    def create_client(self):
        res = call("oauth2.consumer", "create", {
            "name": "FOR TEST - TO BE DELETED (%s)" % time.time(),
            "type": "SYSTEM",
            "profile": "WEB",
        })
        call("oauth2.assignment", "create", {
            "user_id": 1,
            "consumer_id": res,
        })
        client = call("oauth2.consumer", "read", res, ["key", "secret"])
        return client["key"], client["secret"]

