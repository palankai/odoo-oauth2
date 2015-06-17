import os
import urlparse
import xmlrpclib


def endpoint():
    docker_host = os.environ["DOCKER_HOST"]
    p = urlparse.urlparse(docker_host)
    host = p.hostname
    return "http://{host}:8069/auth/token".format(host=host)

def call(obj, method, *args, **kwargs):
    models = xmlrpclib.ServerProxy('http://192.168.59.103:8069/xmlrpc/2/object')
    return models.execute_kw("odoo_oauth2", 1, "admin",
            obj, method,
                args, kwargs)

def get_proxy():
    docker_host = os.environ["DOCKER_HOST"]
    p = urlparse.urlparse(docker_host)
    host = p.hostname
    url = "http://{host}:8069/xmlrpc/2/object/".format(host=host)
    return xmlrpclib.ServerProxy(url)
