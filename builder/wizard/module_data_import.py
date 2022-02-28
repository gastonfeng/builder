__author__ = 'one'

import posixpath
import zipfile
from base64 import decodestring, encodestring
from io import StringIO

from odoo import models, fields


class ModuleImport(models.TransientModel):
    _name = 'builder.data.import.wizard'
    _description = 'ModuleImport'
    path_prefix = fields.Char('Path Prefix')
    file = fields.Binary('File', required=True)

    # @api.one
    def action_import(mself):
        for self in mself:
            f = StringIO()
            f.write(decodestring(self.file))
            zfile = zipfile.ZipFile(f)
            print(self.env.context)

            module = self.env[self.env.context.get('active_model')].search(
                [('id', '=', self.env.context.get('active_id'))])

            for zitem in zfile.filelist:
                if not zitem.orig_filename.endswith('/'):
                    result = module.data_file_ids.create({
                        'path': posixpath.join('/', self.path_prefix or '', zitem.orig_filename),
                        'content': encodestring(zfile.read(zitem)),
                        'module_id': self.env.context.get('active_id')
                    })

            return {'type': 'ir.actions.act_window_close'}
