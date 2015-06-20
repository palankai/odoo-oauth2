from openerp import models, fields
from openerp import _

from .. import conf
from .. import func


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
    assignment_ids = fields.One2many(
        'oauth2.assignment', 'consumer_id', string="Scopes"
    )
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


class Assignment(models.Model):
    _name = 'oauth2.assignment'

    user_id = fields.Many2one('res.users', required=True)
    consumer_id = fields.Many2one('oauth2.consumer', required=True)
    scope = fields.Text(required=False)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "oauth2_assignment_unique_user_consumer",
            "UNIQUE(user_id, consumer_id)",
            _("The user, consumer pair must be unique")
        ),
    ]
