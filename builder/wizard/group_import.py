__author__ = 'one'

from odoo import models, fields


class GroupImport(models.TransientModel):
    _name = 'builder.res.groups.import.wizard'
    _description = 'GroupImport'
    group_ids = fields.Many2many('res.groups', 'builder_res_groups_import_wizard_group_rel', 'wizard_id', 'group_id',
                                 'Groups')
    set_inherited = fields.Boolean('Set as Inherit', default=True)

    # @api.one
    def action_import(self):
        for tself in self:
            group_obj = tself.env['builder.res.groups']
            module = tself.env[tself.env.context.get('active_model')].search(
                [('id', '=', tself.env.context.get('active_id'))])

            for group in tself.group_ids:
                data = tself.env['ir.model.data'].search([('model', '=', group._name), ('res_id', '=', group.id)])
                xml_id = "{module}.{id}".format(module=data.module, id=data.name)

                module_group = tself.env['builder.res.groups'].search(
                    [('module_id', '=', module.id), ('xml_id', '=', xml_id)])

                if not module_group.id:
                    new_group = group_obj.create({
                        'module_id': tself.env.context.get('active_id'),
                        'name': group.name,
                        'inherited': tself.set_inherited,
                        'xml_id': xml_id,
                    })

            return {'type': 'ir.actions.act_window_close'}
