from odoo import models, fields, api

__author__ = 'deimos'


class Superclass(models.AbstractModel):
    _name = 'ir.mixin.polymorphism.superclass'

    subclass_id = fields.Integer('Subclass ID', compute='_compute_res_id')
    subclass_model = fields.Char("Subclass Model", required=True,default=lambda s: s._name)
    #
    # _defaults = {
    #     'subclass_model': lambda s, c, u, cxt=None: s._name
    # }

    # @api.one
    def _compute_res_id(self):
        if self.subclass_model == self._name:
            self.subclass_id = self.id
        else:
            subclass_model = self.env[self.subclass_model]
            attr = subclass_model._inherits.get(self._name)
            if attr:
                self.subclass_id = subclass_model.search([
                    (attr, '=', self.id)
                ]).id
            else:
                self.subclass_id = self.id

    # def fields_view_get(self,  view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
    #     record = self.browse( 2, context=context)
    #     if self._name == record.subclass_model:
    #         view = super(Superclass, self).fields_view_get( view_id, view_type, context=context, toolbar=toolbar, submenu=submenu)
    #     else:
    #         view = self.pool.get(record.subclass_model).fields_view_get( view_id, view_type, context=context, toolbar=toolbar, submenu=submenu)
    #     return view
    #@api.multi
    def get_formview_action(self, access_uid=None):
        """
        @return <ir.actions.act_window>
        """

        record = self[0]
        if not record.subclass_model:
            return super(Superclass, self).get_formview_action()

        create_instance = False
        # try:
        if not record.subclass_id:
            create_instance = True
        # except:
        #     create_instance = True

        if create_instance:
            self.env[record.subclass_model].create_instance(self[0].id)

        if self._name == record.subclass_model:
            view = super(Superclass, self).get_formview_action()
        else:
            view = self.env[record.subclass_model].browse(record.subclass_id).get_formview_action()
        return view

    #@api.one
    def get_instance(self):
        return self.env[self.subclass_model].browse(self.subclass_id)

    @property
    def instance(self):
        return self.env[self.subclass_model].browse(self.subclass_id)

    @api.model
    def create_instance(self, id):
        raise NotImplementedError

    #@api.multi
    def action_edit(self):
        data = self._model.get_formview_action()
        return data


class Subclass(models.AbstractModel):
    _name = 'ir.mixin.polymorphism.subclass'

    def get_formview_id(self, access_uid=None):
        view = self.env['ir.ui.view'].search([
            ('type', '=', 'form'),
            ('model', '=', self._name)
        ])
        return view[0].id if len(view) else False

    #@api.multi
    def unlink(self):
        records = self
        parent_ids = {
            model: [rec[field].id for rec in records] for model, field in self._inherits.items()
        }

        res = super(Subclass, self).unlink()
        if res:
            for model in parent_ids:
                self.env[model].unlink(parent_ids.get(model, []))
        return res
