import base64
import json

from openerp import http
from openerp.http import request

from ..exceptions import (
    InvalidRequestException, AuthenticationException, InvalidClientException,
    InvalidGrantException, InvalidScopeException
)


class Authentication(http.Controller):

    @http.route("/auth/token/", auth="public")
    def index(self, **kw):
        status = 200
        headers = {}
        response = None
        try:
            response = self.process_auth()
        except AuthenticationException, ex:
            response = ex.to_dict()
            status = ex.status
            headers = ex.headers

        return self.response(response, status, headers)

    def process_auth(self):
        if self.get_post("grant_type") == "password":
            return self.password_auth()
        if self.get_post("grant_type") == "refresh_token":
            return self.refresh_token()
        raise InvalidRequestException()

    def password_auth(self):
        consumer = self.get_consumer()
        user = self.get_user()
        self.get_assignment(user, consumer)
        Session = http.request.env['oauth2.session'].sudo()
        session = Session.create({
            "user_id": user.id,
            "consumer_id": consumer.id,
        })
        return dict(
            access_token=session.token,
            token_type="Bearer",
            expires_in=int(session.get_expires_in().total_seconds()),
            refresh_token=session.refresh_token,
            scope=session.scope
        )

    def refresh_token(self):
        self.get_consumer()
        refresh_token = self.get_post("refresh_token")
        session = self.get_session_by_refresh_token(refresh_token)
        session.refresh()

        return dict(
            access_token=session.token,
            token_type="Bearer",
            expires_in=int(session.get_expires_in().total_seconds()),
        )

    def get_consumer(self):
        key, secret = self.get_client_credentials()
        Consumer = http.request.env['oauth2.consumer'].sudo()
        consumer = Consumer.search(
            [("key", "=", key), ("secret", "=", secret)]
        )
        if len(consumer) != 1:
            raise InvalidClientException()
        return consumer

    def get_user(self):
        username = self.get_post("username")
        password = self.get_post("password")
        User = http.request.env['res.users'].sudo()
        user = User.search([("login", "=", username)])
        if not user:
            raise InvalidGrantException()
        try:
            user.check_credentials(password)
        except:
            raise InvalidGrantException()
        return user

    def get_assignment(self, user, consumer):
        Assignment = http.request.env['oauth2.assignment'].sudo()
        assignment = Assignment.search([
            ("user_id", "=", user.id),
            ("consumer_id", "=", consumer.id)
        ])
        if not assignment:
            raise InvalidGrantException()
        return assignment

    def get_session_by_refresh_token(self, refresh_token):
        Session = http.request.env['oauth2.session'].sudo()
        session = Session.search([
            ("refresh_token", "=", refresh_token)
        ])
        if not session:
            raise InvalidGrantException()
        return session


    def get_client_credentials(self):
        header = self.get_header("authorization")
        if not header: raise InvalidClientException()
        auth = header.split()
        if len(auth) != 2: raise InvalidClientException()
        if auth[0].lower() != "basic": raise InvalidClientException()
        try:
            return base64.b64decode(auth[1]).split(":")
        except TypeError:
            raise InvalidClientException()

    def response(self, response, status, headers):
        http_headers = {
            "Cache-Control": "no-store",
            "Pragma": "no-cache"
        }
        http_headers.update(headers)
        return http.Response(
            json.dumps(response),
            content_type="application/json",
            status=status,
            headers=http_headers
        )

    def get_post(self, name):
        return request.httprequest.form.get(name)

    def get_header(self, name):
        return request.httprequest.headers.get(name)
