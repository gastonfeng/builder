# -*- coding: utf-8 -*-
import logging
import os

import sys
import zipfile
from ftplib import FTP

logging.basicConfig(level=logging.INFO)
from mywork.tools.odoo import odoo

modulename = 'builder'

BUILD_NUMBER = open('build.info').read().strip()
urls = 'http://www.kaikong.com.cn/odoo/%s%s.zip' % (modulename, str(BUILD_NUMBER))

try:
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
    ftp.quit()

    logging.info('->kaikong')
    lohost = odoo('localhost', '8888', 'kaikong', 'kaikong@kaikong.com.cn', '41701015')
    logging.info(lohost.ver())
    lohost.toLogin()
    lohost.install_from_urls(modulename, urls)
    logging.info('test ok')

    logging.info('test with woniu66')
    woniu = odoo('www.woniu66.com', '8808')
    woniu.create_test_db()
    # 本模块依赖software模块,由于不是系统模块,新系统找不到模块文件(数据库删除时会清除模块),需要先安装
    swver = open('../odoo_software/build.info').read().strip()
    zipurl = 'http://app.woniu66.com/odoo/software%s.zip' % str(swver)
    woniu.install_from_urls('software', zipurl)
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

