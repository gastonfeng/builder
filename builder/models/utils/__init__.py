from odoo import api


def simple_selection(model, value_field, label_field=None, domain=None):
    domain = domain or []
    label_field = label_field or value_field

    @api.model
    def _selection_function(self):
        return [(getattr(c, value_field), getattr(c, label_field)) for c in self.env[model].search(domain)]
    return _selection_function


def get_field_types(model):
    context = {}
    # Avoid too many nested `if`s below, as RedHat's Python 2.6
    # break on it. See bug 939653.
    return sorted([(k, k) for k in
                   ['one2many', 'many2one', 'many2many', 'binary', 'char', 'boolean', 'date', 'datetime', 'float',
                    'html', 'integer', 'reference', 'selection', 'serialized', 'text']])
