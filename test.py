# -*- coding: utf-8 -*-
import logging

import sys

logging.basicConfig(level=logging.INFO)
from mywork.tools.odoo import odoo

modulename = 'builder'

BUILD_NUMBER = open('build.info').read().strip()
urls = 'http://app.woniu66.com/odoo/%s%s.zip' % (modulename, str(BUILD_NUMBER))

try:
    logging.info('->kaikong')
    lohost = odoo('localhost', '8888', 'kaikong', 'kaikong@kaikong.com.cn', '41701015')
    logging.info(lohost.ver())
    lohost.toLogin()
    lohost.install_from_urls(modulename, urls)
    logging.info('test ok')

    logging.info('test with woniu66')
    woniu = odoo('www.woniu66.com', '8808')
    woniu.create_test_db()
    woniu.install_from_urls(modulename, urls)
    logging.info('test ok')


    logging.info('->123.207.157.205:8801')
    lohost = odoo('123.207.157.205', '8801', 'kaikong', 'kaikong@kaikong.com.cn', '41701015')
    lohost.toLogin()
    lohost.install_from_urls(modulename, urls)
    logging.info('finished.')
    sys.exit(0)
except Exception, e:
    logging.error(e)
    sys.exit(1)
