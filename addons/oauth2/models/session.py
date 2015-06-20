import datetime
from openerp import models, fields

from .. import func


class Session(models.Model):
    _name = 'oauth2.session'
    _log_access = False

    token = fields.Char(size=255, required=True, default=lambda self: func.create_token())
    created = fields.Datetime(required=True, default=lambda self: datetime.datetime.utcnow())
    expires_at = fields.Datetime(required=True, default=lambda self: datetime.datetime.utcnow()+datetime.timedelta(hours=1))
    refresh_token = fields.Char(size=255, default=lambda self: func.create_token())
    user_id = fields.Many2one('res.users', required=True, ondelete="cascade")
    consumer_id = fields.Many2one('oauth2.consumer', required=True, ondelete="cascade")
    scope = fields.Text(required=False)

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

    def get_expires_in(self):
        expires_at = fields.Datetime.from_string(self.expires_at)
        return expires_at - datetime.datetime.utcnow()

    def refresh(self):
        self.write({
            "token": func.create_token(),
            "expires_at": datetime.datetime.utcnow()+datetime.timedelta(hours=1)
        })
