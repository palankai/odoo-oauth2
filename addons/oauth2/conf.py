from openerp import _


CONSUMER_TYPES = (
    ("SYSTEM", _("system")),
    ("CONFID", _("confidential")),
    ("PUBLIC", _("public")),
)


CONSUMER_PROFILES = (
    ("WEB", _("web")),
    ("BROWSER", _("user agent based")),
    ("NATIVE", _("native")),
)


DEFAULT_TOKEN_LENGTH=64
