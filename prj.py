# coding=utf-8
from mywork.project.odooModule import odooModule
from mywork.project.project import project
from mywork.stocks.gits import gits
from mywork.tools._jenkins import jenkins_task, jenkins_server
from mywork.tools.build_odoo import build_odoo
from mywork.workSpace.store import store

de = odooModule('developer')
de.url = 'http://kaikong.com.cn/odoo/developer.zip'
sw = odooModule('software')
sw.url = 'http://kaikong.com.cn/odoo/software.zip'

om = build_odoo('builder', "1.0", git=gits('builder', url='ssh://kaikong@192.168.31.10/home/git/odoo_builder.git'),
                jenkins_task=jenkins_task('odoo_builder', runWith=jenkins_server('ubuntu16')),
                store=store('kaikong.com.cn'), deploy=['www.kaikong.cn', ],
                depends=[de, sw, ])
prj = project('builder', products=[om, ], )
prj.output('builder')
prj.build()
