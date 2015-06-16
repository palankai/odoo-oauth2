class AuthenticationException(Exception):
    error = None
    description = None
    uri = "http://tools.ietf.org/html/rfc6749"
    status = 400
    headers = {}

    def __init__(self):
        super(AuthenticationException, self).__init__(self.error)

    def to_dict(self):
        return { "error": self.error,
            "error_description": self.description,
            "error_uri": self.uri }


class InvalidRequestException(AuthenticationException):
    error = "invalid_request"
    description = "The request is missing a required parameter, includes an unsupported parameter value " \
    "(other than grant type), repeats a parameter, includes multiple credentials, utilizes more than one " \
    "mechanism for authenticating the client, or is otherwise malformed."


class InvalidClientException(AuthenticationException):
    status = 401
    headers = {
       'WWW-Authenticate': 'Basic realm="OAuth2"'
    }
    error = "invalid_client"
    description = "Client authentication failed (e.g., unknown client, no client authentication included, or " \
    "unsupported authentication method).  The authorization server MAY return an HTTP 401 (Unauthorized) status code " \
    "to indicate which HTTP authentication schemes are supported.  If the client attempted to authenticate via the " \
    "\"Authorization\" request header field, the authorization server MUST respond with an HTTP 401 (Unauthorized) " \
    "status code and include the \"WWW-Authenticate\" response header field matching the authentication scheme used " \
    "by the client."


class InvalidGrantException(AuthenticationException):
    status = 403
    error = "invalid_grant"
    description = "The provided authorization grant (e.g., authorization code, resource owner credentials) or " \
    "refresh token is invalid, expired, revoked, does not match the redirection URI used in the authorization " \
    "request, or was issued to another client."


class UnauthorizedClientException(AuthenticationException):
    status = 403
    error = "unauthorized_client"
    description = "The authenticated client is not authorized to use this authorization grant type."


class UnsupportedGrantTypeException(AuthenticationException):
    error = "unsupported_grant_type"
    description = "The authorization grant type is not supported by the authorization server."


class InvalidScopeException(AuthenticationException):
    status = 403
    error = "invalid_scope"
    description = "The requested scope is invalid, unknown, malformed, or exceeds the scope granted by "
    "the resource owner."


