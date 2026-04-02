from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid

class ResGroups(models.Model):
    _inherit = "res.groups"

    uuid = fields.Char(
        string="uuid",
        default=lambda self: f"uuid_{uuid.uuid4().hex}",
        readonly=True,
        required=True,
        copy=False,
    )

class ResGroupsPrivilege(models.Model):
    _inherit = "res.groups.privilege"

    uuid = fields.Char(
        string="uuid",
        default=lambda self: f"uuid_{uuid.uuid4().hex}",
        readonly=True,
        required=True,
        copy=False,
    )
