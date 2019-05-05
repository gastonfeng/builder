import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ir_cron(models.Model):
    """ Model describing cron jobs (also called actions or tasks).
    """

    # TODO: perhaps in the future we could consider a flag on ir.cron jobs
    # that would cause database wake-up even if the database has not been
    # loaded yet or was already unloaded (e.g. 'force_db_wakeup' or something)
    # See also openerp.cron

    _name = "builder.ir.cron"
    _order = 'name'
    module_id = fields.Many2one('builder.ir.module.module', 'Module', ondelete='cascade')
    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active',default=1)
    interval_number = fields.Integer('Interval Number', help="Repeat every x.",default=1)
    interval_type = fields.Selection([('minutes', 'Minutes'),
                                      ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                      ('weeks', 'Weeks'), ('months', 'Months')], 'Interval Unit',default='months')
    numbercall = fields.Integer('Number of Calls',
                                help='How many times the method is called,\na negative number indicates no limit.',default=1)
    doall = fields.Boolean('Repeat Missed',
                           help="Specify if missed occurrences should be executed when the server restarts.")
    nextcall = fields.Datetime('Next Execution Date', help="Next planned execution date for this job.")
    model_id = fields.Many2one('builder.ir.model', 'Object',
                               help="Model name on which the method to be called is located, e.g. 'res.partner'.")
    model_method_id = fields.Many2one('builder.ir.model.method', 'Method',
                                      help="Name of the method to be called when this job is processed.")
    args = fields.Text('Arguments', help="Arguments to be passed to the method, e.g. (uid,).")
    priority = fields.Integer('Priority',
                              help='The priority of the job, as an integer: 0 means higher priority, 10 means lower priority.',default=5)

    # _defaults = {
    #     'priority': 5,
    #     'interval_number': 1,
    #     'interval_type': 'months',
    #     'numbercall': 1,
    #     'active': 1,
    # }

    def _check_args(self):
        try:
            for this in self.browse(self._ids):
                pass
                # str2tuple(this.args)
        except Exception:
            return False
        return True

    _constraints = [
        (_check_args, 'Invalid arguments', ['args']),
    ]

    def toggle(self, ids, model, domain):
        active = bool(self.env[model].search_count(domain))

        return self.try_write(ids, {'active': active})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
