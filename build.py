# -*- coding: utf-8 -*-
import logging
import os
import sys
import zipfile
from ftplib import FTP

from mywork.resources.odoo_kaikong import odoo_centos, odoo_woniu66

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
    'name': 'Module Builder',
    'version': '%s',
    'category': 'Programming',
    'summary': 'Build your modules right inside Odoo',
    'description': """
This module aims to help in the development of new modules
=======================================================================================

""",
    'author': 'Soluciones Moebius',
    #"license": "AGPL-3",
    'website': 'http://www.solucionesmoebius.com/',
    'depends': ['web', 'web_diagram', 'website','software'],
    'data': [
        # 'security/base_security.xml',
        # 'security/ir.model.access.csv',

        'data/oe.css.classes.yml',
        'wizard/module_generate_view.xml',
        'wizard/model_lookup_wizard_view.xml',
        'wizard/menu_lookup_wizard_view.xml',
        'wizard/action_lookup_wizard_view.xml',
        'wizard/website_asset_bulk_add_view.xml',
        'wizard/website_media_item_bulk_add_view.xml',
        'wizard/website_page_import_view.xml',
        'wizard/model_access_generate_wizard_view.xml',
        'wizard/demo_creator_wizard_view.xml',

        'views/views/base_view.xml',
        'views/views/calendar_view.xml',
        'views/views/form_view.xml',
        'views/views/gantt_view.xml',
        'views/views/graph_view.xml',
        'views/views/kanban_view.xml',
        'views/views/search_view.xml',
        'views/views/tree_view.xml',
        'views/views/selector_view.xml',
        'views/website_view.xml',

        'views/demo/char_views.xml',
        'views/demo/name_views.xml',
        'views/demo/email_views.xml',
        'views/demo/autoincrement_views.xml',
        'views/demo/selection_views.xml',
        'views/demo/normal_views.xml',
        'views/demo/custom_list_views.xml',
        'views/demo/m2o_views.xml',
        'views/demo/m2m_views.xml',
        'views/demo/date_views.xml',
        'views/demo/binary_views.xml',

        'wizard/module_data_import_view.xml',
        'wizard/module_import_view.xml',
        'wizard/module_export_view.xml',
        'wizard/model_import_view.xml',
        'wizard/group_import_view.xml',

        'views/menu_view.xml',
        'views/module_view.xml',
        'views/field_view.xml',
        'views/model_view.xml',
        'views/res_config_model_view.xml',
        'views/action_view.xml',
        'views/data_view.xml',
        'views/security_view.xml',
        'views/cron_view.xml',
        'views/workflow_view.xml',
        'views/menu.xml',

        'views/backend_assets.xml',
        'views/snippet_templates.xml',
        'views/designer/website_page_designer.xml',
        'views/designer/designer_snippets.xml',

        'security/ir.model.access.csv',
    ],
    'test': [
        'test/test_demo.yml',
    ],
    'images': [
        'static/description/module_info.png',
        'static/description/designer.png',
    ],
    #'qweb': [],
     # 'qweb': ['static/src/xml/templates.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
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
    odoo_woniu66.install_from_urls(modulename, urls)

    # shutil.copyfile(zipname, 'z:/download/odoo_app/builder.zip')
    # shutil.copyfile('build.info', 'z:/download/odoo_app/builder_build')
    cmd = "rsync -avzP --password-file=rsyncd.password builder*.zip rsync://kaikong@www.woniu66.com:/server01/app/odoo"
    os.subprocess.call(cmd, shell=True)
    logging.info('finished.')
    sys.exit(0)
except Exception, e:
    logging.error(e)
    sys.exit(-1)
