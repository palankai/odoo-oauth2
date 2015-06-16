import datetime
import json

from openerp import http
from openerp.http import request

from ..exceptions import InvalidRequestException, AuthenticationException


class Authentication(http.Controller):

    @http.route("/auth/token/", auth="public")
    def index(self, **kw):
        status = 200
        headers = {}
        response = None
        try:
            response = self.process()
        except AuthenticationException, ex:
            response = ex.to_dict()
            status = ex.status
            headers = ex.headers

        return self.response(response, status, headers)

    def process(self):
        if self.get_post("grant_type") == "password":
            return self.password_auth()
        if self.get_post("grant_type") == "refresh_token":
            return self.refresh_token()
        raise InvalidRequestException()

    def password_auth(self):
        if not self.get_header("authorization"):
            raise InvalidRequestException()
        return "Pass"

    def refresh_token(self):
        return "Refresh"

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

