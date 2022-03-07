__author__ = 'one'

from odoo import models, fields


class ModelAccessGenerateWizard(models.TransientModel):
    _name = 'builder.ir.model.access.generate.wizard'
    _description = 'ModelAccessGenerateWizard'
    module_id = fields.Many2one('builder.ir.module.module', 'Module', ondelete='CASCADE')
    model_ids = fields.Many2many('builder.ir.model', 'builder_ir_model_access_generate_model_rel', 'wizard_id',
                                 'model_id', 'Models')
    group_ids = fields.Many2many('builder.res.groups', 'builder_ir_model_access_generate_group_rel', 'wizard_id',
                                 'group_id', 'Groups')

    perm_read = fields.Boolean('Read Access')
    perm_write = fields.Boolean('Write Access')
    perm_create = fields.Boolean('Create Access')
    perm_unlink = fields.Boolean('Delete Access')

    # @api.one
    def action_generate(self):
        for SELF in self:
            access_obj = SELF.env['builder.ir.model.access']

            for model in SELF.model_ids:
                for group in SELF.group_ids:
                    access_obj.create({
                        'module_id': SELF.module_id.id,
                        'model_id': model.id,
                        'group_id': group.id,
                        'perm_read': SELF.perm_read,
                        'perm_create': SELF.perm_create,
                        'perm_unlink': SELF.perm_unlink,
                        'perm_write': SELF.perm_write,
                        'name': "{name} {module}_{group}".format(name=model.model.replace('.', '_'),
                                                                 module=SELF.module_id.name, group=group.xml_id)
                    })

            return {'type': 'ir.actions.act_window_close'}
