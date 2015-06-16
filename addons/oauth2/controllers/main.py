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
            response = self.process(request)
        except AuthenticationException, ex:
            response = ex.to_dict()
            status = ex.status
            headers = ex.headers

        return self.response(response, status, headers)

    def process(self, r):
        if self.get_param(r, "grant_type") == "password":
            return self.password_auth(r)
        if self.get_param(r, "grant_type") == "refresh_token":
            return self.refresh_token(r)
        raise InvalidRequestException()

    def get_param(self, r, name):
        return r.params.get("grant_type", "None")

    def password_auth(self, r):
        return "Pass"

    def refresh_token(self, r):
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
