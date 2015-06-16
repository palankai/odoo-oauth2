from openerp import models, fields
from openerp import _

from .. import conf
from .. import func


class Session(models.Model):
    _name = 'oauth2.session'
    _log_access = False

    token = fields.Char(size=255, required=True)
    created = fields.Datetime(required=True)
    expires_at = fields.Datetime(required=True)
    refresh_token = fields.Char(size=255)
    user_id = fields.Many2one('res.users', required=True)
    consumer_id = fields.Many2one('oauth2.consumer', required=True)

    _sql_constraints = [
        (
            "oauth2_session_unique_token",
            "UNIQUE(token)",
            "The token must be unique"
        ),
        (
            "oauth2_session_unique_refresh_token",
            "UNIQUE(refresh_token)",
            "The refresh token must be unique"
        ),
    ]

