import datetime
from openerp import exceptions
from openerp import fields


def get_session(request, token):
    Session = request.env['oauth2.session'].sudo()
    session = Session.search([
        ("token", "=", token),
        ("expires_at", ">", fields.Datetime.to_string(datetime.datetime.utcnow()))
    ])
    if not session:
        raise exceptions.AccessDenied()
    return session

