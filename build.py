# -*- coding: utf-8 -*-
import logging
import os
import sys
import zipfile
from ftplib import FTP

from mywork.resources.odoo_kaikong import odoo_centos

logging.basicConfig(level=logging.INFO)
from mywork.tools.odoo import odoo

modulename = 'builder'

BUILD_NUMBER = open('build.info').read().strip()
urls = 'http://kaikong.com.cn/odoo/%s%s.zip' % (modulename, str(BUILD_NUMBER))

try:
    from ver_build import BUILD_NUMBER

    ver = '1.' + str(BUILD_NUMBER)
    erp = '''# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': '设备数据采集模块',
    'version': '%s',
    'depends': [],
    'author': 'gastonfeng',
    "website" : "http://www.woniu66.com",
    "category" : "指定行业应用",
    "licence" : "AGPL-3",
    "description": """
设备数据采集模块
====================================
设备数据采集模块
                    """,
    "data" : [
        'views/views.xml',
        'views/actions.xml',
        'views/menu.xml',
        ],
    "demo" : [],
    "installable": True,
    'auto_install': True,
    'application': True,
}
''' % ver

    f = os.path.join(os.path.abspath(os.path.curdir), 'builder/__openerp__.py')
    stream = file(f, 'w')
    stream.write(erp)
    stream.close()


    zipname = modulename + str(BUILD_NUMBER) + '.zip'
    f = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    startdir = "."
    for dirpath, dirnames, filenames in os.walk(startdir):
        l = len(dirpath)
        if l > 4:
            d = dirpath[2]
        if l > 4 and d == '.':
            continue
        for filename in filenames:
            if filename == zipname:
                continue
            f.write(os.path.join(dirpath, filename))
    f.close()

    ftp = FTP()
    ftp.connect('kaikong.gotoftp4.com', '21')
    ftp.login('kaikong', 'gaston701125')
    ftp.cwd('wwwroot/odoo')
    bufsize = 1024
    file_handler = open(zipname, 'rb')
    ftp.storbinary('STOR %s' % os.path.basename(zipname), file_handler, bufsize)
    ftp.set_debuglevel(0)
    file_handler.close()
    file_handler = open(zipname, 'rb')
    ftp.storbinary('STOR %s' % os.path.basename(modulename + '.zip'), file_handler, bufsize)
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()

    logging.info('test with full')
    lohost = odoo('localhost', '8069', 'odoo10', 'gastonfeng@gmail.com', 'gaston701125')
    logging.info(lohost.ver())
    lohost.toLogin()
    lohost.install_from_urls(modulename, urls)
    logging.info('test ok')

    logging.info('test with new db')
    woniu = odoo('localhost', '8069')
    woniu.create_test_db()
    woniu.install_from_urls(modulename, urls)
    logging.info('test ok')

    odoo_centos.install_from_urls(modulename, urls)

    # shutil.copyfile(zipname, 'z:/download/odoo_app/builder.zip')
    # shutil.copyfile('build.info', 'z:/download/odoo_app/builder_build')
    logging.info('finished.')
    sys.exit(0)
except Exception, e:
    logging.error(e)
    sys.exit(-1)
