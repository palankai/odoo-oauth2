import os
import urlparse

_endpoint=None

def endpoint():
    docker_host = os.environ["DOCKER_HOST"]
    p = urlparse.urlparse(docker_host)
    host = p.hostname
    return "http://{host}:8069/auth/token/".format(host=host)
