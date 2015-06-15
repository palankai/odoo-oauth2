from openerp import models, fields
from openerp import _

import conf
import func


class Consumer(models.Model):
    _name = 'oauth2.consumer'

    key = fields.Char(
        _("Key"), size=128, required=True,
        default=lambda self: func.create_token()
    )
    secret = fields.Char(
        _("Secret"), size=128, required=True,
        default=lambda self: func.create_token()
    )
    name = fields.Char(_("Consumer name"), size=100, required=True)
    description = fields.Text(_("Description"))
    type = fields.Selection(
        string=_("Consumer type"), selection=conf.CONSUMER_TYPES,
        required=True
    )
    profile = fields.Selection(
        string=_("Consumer profile"), selection=conf.CONSUMER_PROFILES,
        required=True
    )
    redirect_uri = fields.Char(_("Redirect URI"), size=254)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "oauth2_consumer_unique_name",
            "UNIQUE(name)",
            _("The name must be unique")
        ),
        (
            "oauth2_consumer_unique_key",
            "UNIQUE(key)",
            _("The key must be unique")
        ),
    ]


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

