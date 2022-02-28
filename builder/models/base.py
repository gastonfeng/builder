from odoo import _
from odoo import models, fields, api


class ModelDependency(models.Model):
    _name = 'builder.ir.module.dependency'
    _description = 'ModelDependency'
    DEPENDENCY_TYPES = [
        ('module', _('Module')),
        ('project', _('Module Project')),
        ('manual', _('Module Name')),
    ]

    name = fields.Char('Name', compute='_compute_name')
    # the module that depends on it
    module_id = fields.Many2one('builder.ir.module.module', 'Module', ondelete='cascade')

    type = fields.Selection(DEPENDENCY_TYPES, 'Type', default='manual', store=False, search=True)

    # the module corresponding to the dependency, and its status
    dependency_module_id = fields.Many2one('ir.module.module', 'Dependency module', store=False, search=True)
    dependency_project_id = fields.Many2one('builder.ir.module.module', 'Dependency project', store=False, search=True)
    dependency_module_name = fields.Char('Dependency', index=True)

    # @api.one
    @api.depends('dependency_module_id', 'dependency_project_id', 'dependency_module_name')
    def _compute_name(mself):
        for self in mself:
            self.dependency_module_name = self.name = self.dependency_module_id.name or self.dependency_project_id.name or self.dependency_module_name


class OeCssClass(models.Model):
    _name = 'builder.web.util.css.class'
    _description = 'OeCssClass'
    _order = 'name'
    _log_access = False

    name = fields.Char(string='Name', required=True)
    usage = fields.Char(string='Usage')
