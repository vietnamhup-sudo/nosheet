from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

FB_LIVECHAT_CHANNEL = "Facebook"

class Password(models.TransientModel):
    _name = 'nosheet.password'
    _description = 'Nosheet Password'

    password = fields.Char(string='Password')

    def action_confirm(self):
        self.ensure_one()
        data = self.password
        self.password = ""

        return {
            'infos': {
                'value': data
            }
        }
