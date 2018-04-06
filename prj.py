# coding=utf-8
from mywork.project.project import project
from mywork.stocks.gits import gits
from mywork.tools._jenkins import jenkins_task, jenkins_server
from mywork.tools.build_odoo import build_odoo
from mywork.workSpace.store import store

om = build_odoo('builder', git=gits('builder', url='ssh://kaikong@192.168.31.10/home/git/odoo_builder.git'),
                jenkins_task=jenkins_task('odoo_builder', runWith=jenkins_server('ubuntu16')),
                store=store('kaikong.com.cn'))
prj = project('builder', products=[om, ], )
prj.build()
prj.output('builder')
