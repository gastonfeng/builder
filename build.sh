#!/usr/bin/env bash
yum install rsync python-setuptools -y
python -V
rm *.zip -rf
easy_install odoorpc
rm -rf /var/log/odoo/odoo-server.log
python gen_openerp.py
python build.py
cat /var/log/odoo/odoo-server.log
chmod 600 rsyncd.password
rsync -avzP --password-file=rsyncd.password builder*.zip rsync://kaikong@www.woniu66.com:/server01/app/odoo
