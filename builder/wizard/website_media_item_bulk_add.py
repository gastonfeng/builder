__author__ = 'one'

from odoo import models, fields


class MediaItemBulkAddWizard(models.TransientModel):
    _name = 'builder.website.media.item.bulk.add.wizard'
    _description = 'MediaItemBulkAddWizard'
    module_id = fields.Many2one('builder.ir.module.module', 'Module', ondelete='CASCADE')
    data_ids = fields.Many2many('builder.data.file', 'builder_website_media_item_bulk_data_file_rel', 'wizard_id',
                                'data_id', 'Files')

    # @api.one
    def action_import(self):
        for SELF in self:
            media_item_model = SELF.env['builder.website.media.item']

            for data_file in SELF.data_ids:
                new_item = media_item_model.create({
                    'file_id': data_file.id,
                    'module_id': SELF.module_id.id,
                })

            return {'type': 'ir.actions.act_window_close'}
