import datetime
from openerp import models, fields

from .. import func

class Session(models.Model):
    _name = 'oauth2.session'
    _log_access = False

    token = fields.Char(size=255, required=True, default=lambda self: func.create_token())
    created = fields.Datetime(required=True, default=lambda self: datetime.datetime.utcnow())
    expires_at = fields.Datetime(required=True, default=lambda self: datetime.datetime.utcnow()+datetime.timedelta(hours=1))
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

