import datetime

from openerp.exceptions import AccessDenied
from openerp.tests import common

from .. import api


class TestOAuth2API(common.TransactionCase):

    def test_get_session(self):
        session = self.create_session()
        token = "GENERATED"
        api_session = api.get_session(self, token)
        self.assertEqual(session.id, api_session.id)

    def test_get_session_with_invalid_token(self):
        token = "GENERA"
        with self.assertRaises(AccessDenied):
            api.get_session(self, token)

    def test_get_session_with_expired_token(self):
        session = self.create_expired_session()
        token = "GENERATED"
        with self.assertRaises(AccessDenied):
            api.get_session(self, token)

    def create_session(self):
        consumer = self.env["oauth2.consumer"].sudo().create({
            "name": "FOR TEST - TO BE DELETED BY TRANSACTION",
            "type": "SYSTEM",
            "profile": "WEB"
        })
        return self.env["oauth2.session"].sudo().create({
            "user_id": 1,
            "consumer_id": consumer.id,
            "token": "GENERATED",
            "refresh_token": "REFRESH",
            "expires_at": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        })
    
    def create_expired_session(self):
        consumer = self.env["oauth2.consumer"].sudo().create({
            "name": "FOR TEST - TO BE DELETED BY TRANSACTION",
            "type": "SYSTEM",
            "profile": "WEB"
        })
        return self.env["oauth2.session"].sudo().create({
            "user_id": 1,
            "consumer_id": consumer.id,
            "token": "GENERATED",
            "refresh_token": "REFRESH",
            "expires_at": datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        })
