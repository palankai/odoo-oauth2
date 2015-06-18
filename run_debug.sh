#!/bin/bash

docker build -t odoo-oauth2-debug odoo/
docker run -ti --rm -p 8069:8069 -v $(pwd)/addons:/mnt/extra-addons -v $(pwd)/odoo/config:/etc/odoo odoo-oauth2-debug

