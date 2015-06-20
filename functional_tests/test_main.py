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
        i, k, s = self.create_client()
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
        j = r.json()
        self.assertEqual(j["token_type"], "Bearer")
        self.assertIn("access_token", j)
        self.assertIn("expires_in", j)
        self.assertIn("refresh_token", j)
        self.assertIn("scope", j)
        session = self.read_session(j["access_token"])
        self.assertEqual(session["consumer_id"][0], i)
        self.assertEqual(session["user_id"][0], 1)
        self.assertEqual(session["refresh_token"], j["refresh_token"])

    def test_refresh_token(self):
        i, k, s = self.create_client()
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
        j = r.json()
        refresh_token = j["refresh_token"]
        r = requests.post(
            endpoint(), 
            {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }, headers={
                "Authorization":"basic %s" % base64.b64encode("%s:%s" % (k,s))
            }
        )
        j = r.json()
        self.assertEqual(j["token_type"], "Bearer")
        self.assertIn("access_token", j)
        self.assertIn("expires_in", j)
        session = self.read_session(j["access_token"])
        self.assertEqual(session["consumer_id"][0], i)
        self.assertEqual(session["user_id"][0], 1)

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
        return client["id"], client["key"], client["secret"]
    
    def read_session(self, access_token):
        res = call("oauth2.session", "search_read", [("token", "=", access_token)])
        return res[0]
