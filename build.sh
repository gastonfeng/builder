#!/usr/bin/env bash
yum install rsync python-setuptools -y
python -V
rm *.zip -rf
easy_install odoorpc
chmod 600 rsyncd.password
rm -rf /var/log/odoo/odoo-server.log
python mywork/tools/build_odoo.py
