from openerp import http


class Authentication(http.Controller):

    @http.route('/auth/token/', auth='public')
    def index(self, **kw):
        return http.Response("", content_type="application/json")
