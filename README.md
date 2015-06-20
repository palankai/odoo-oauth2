# Odoo OAuth2 Provider

This module provides standard API for authentication.

You can register consumers, and assign users to it.
Then with knowledge of consumer key and secret and user credentials,
you can authenticate and can access resources.

## Provides

- /auth/token/ interface to authenticate

# ToDo

- [x] Client auth
- [x] Token refresh
- [x] API for applications

# Usage

```python
from openerp.addons import oauth2
session = oauth2.get_session("token")
```
