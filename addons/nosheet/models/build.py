from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os
import shutil

previous_stage = {
    '2': '1',
    '3': '2',
    '4': '1',
}

class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    is_custom = fields.Boolean(string="Is Custom")

    @api.constrains('name', 'parent_id', 'is_custom')
    def _check_unique_name_parent(self):
        for rec in self:
            if not rec.name:
                continue

            domain = [
                ('id', '!=', rec.id),
                ('name', '=', rec.name),
                ('parent_id', '=', rec.parent_id.id),
                ('is_custom', '=', True),
            ]

            if self.search_count(domain):
                raise ValidationError(
                    f"Menu {rec.name} already exists under the same parent."
                )

class IrModelFields(models.Model):
    _inherit = "ir.model.fields.selection"

    selected_model_id = fields.Many2one(
        'ir.model', 
        string='Model',
        domain=[('state', '=', 'manual')]
    )

    @api.onchange('selected_model_id')
    def _onchange_selected_model_id(self):
        for record in self:
            if record.selected_model_id:
                record.value = record.selected_model_id.model
                record.name = record.selected_model_id.name
            else:
                record.value = ""
                record.name = ""

    @api.onchange('value')
    def _onchange_value(self):
        for record in self:
            if record.selected_model_id:
                return

            if record.value:
                record.name = record.value
            else:
                record.name = ""

class Build(models.TransientModel):
    _name = 'nosheet.build'
    _description = 'Build'

    def get_title(self, step):
        return {
            '1': _('Pick Options'),
            '2': _('Enter Model Name'),
            '3': _('Create or Select Module'),
            '4': _('Select Model to Edit or Delete'),
        }.get(step)

    action_type = fields.Selection(
            selection=[
                ('create', 'Create'),
                ('edit', 'Edit'),
                ('delete', 'Delete'),
            ],
            string='Action',
            default='create',
            required=True,
        )
    mode = fields.Selection(
            selection=[
                ('model', 'Model'),
                ('menu', 'Menu'),
            ],
            string='Mode',
            default='model',
            required=True,
            readonly=True,
        )
    stage = fields.Selection(
            selection=[
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('4', '4'),
            ],
            string='Action',
            default='2',
            required=True,
        )
    model_description = fields.Char(string='Name')
    model_name = fields.Char(
        string='Name', 
        default=lambda self: f"x_{uuid.uuid4().hex}",
    )
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        domain=[('state', '=', "manual")],
    )
    custom_app_id = fields.Many2one(
        "nosheet.custom.app",
        string="Custom App",
    )

    def go_to_stage(self):
        return {
            'type': 'ir.actions.act_window',
            'name': self.get_title(self.stage),
            'res_model': 'nosheet.build',
            'view_mode': 'form',
            'target': 'new',

            'res_id': self.id,
            'context': {
                **self.env.context,
            },
        }
    def confirm_stage_1(self):
        if self.action_type == 'delete':
            self.stage = '4'
        elif self.action_type == 'edit':
            self.stage = '4'
        else:
            self.stage = '2'

        return self.go_to_stage()

    def confirm_stage_2(self):
        self.stage = '3'
        return self.go_to_stage()

    def confirm_stage_3(self):
        self = self.with_context(create_views_menu_access=True)
        self.create_model()
    
    def add_views_menu_and_access(self, model_name, parent_menu_id):
        model_id = self.env["ir.model"].search([("model", "=", model_name)], limit=1)
        self.create_tree_view_id(model_id.model)
        self.create_form_view_id(model_id.model)
        self.create_search_view_id(model_id.model)
        self.create_model_access(model_id.id, model_id.model)

        self.create_menu(model_id.name, model_id.model, parent_menu_id)

    def clean_up_model(self, model=False):
        actions = self.env["ir.actions.act_window"].search([('res_model', '=', model.model)])
        sequences = self.env["ir.sequence"].search([('code', '=', model.model)])
        filters = self.env["ir.filters"].search([('model_id', '=', model.model)])
        for action in actions:
            menus = self.env['ir.ui.menu'].search([('action', '=', f"ir.actions.act_window,{action.id}")])
            menus.unlink()
            action.unlink()
        sequences.unlink()
        filters.unlink()
        model.view_ids.unlink()
        return model

    def confirm_stage_4(self):
        if self.action_type == 'delete':
            self.model_id.unlink()
        elif self.action_type == 'edit':
            return self.action_open_ir_model()

    def action_open_ir_model(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "IR Model",
            "res_model": "ir.model",
            "view_mode": "form",
            "view_id": self.env.ref("nosheet.view_nosheet_ir_model_form").id,
            "res_id": self.model_id.id,
            "target": "current",
        }

    def previous(self):
        self.stage = previous_stage.get(self.stage, '1')
        return self.go_to_stage()
    
    def create_model_access(self, model_id, model_name):
        self.env["ir.model.access"].create(
            {
                "name": f"Quyền cơ bản",
                "model_id": model_id,
                "group_id": self.env.ref("base.group_user").id,
                "perm_read": True,
                "perm_write": True,
                "perm_create": True,
                "perm_unlink": True,
            }
        )

    def create_model(self):
        model_id = self.env['ir.model'].create(
            {
                "name": self.model_description,
                "model": self.model_name,
                "from_app_id": self.custom_app_id.id,
                "state": "manual",
                "is_mail_thread": True,
                "is_mail_activity": True,
                "is_filter_manual": True
            }
        )

        return model_id

    def create_menu(self, name, model, parent_menu_id):
        if not parent_menu_id:
            raise ValidationError("Parent menu is required to create menu.")
        action_id = self.create_model_act_window(name, model)

        return self.env["ir.ui.menu"].create(
            {
                "name": name,
                "parent_id": parent_menu_id,
                "action": f"ir.actions.act_window,{action_id.id}",
                "is_custom": True,
            }
        )

    def create_model_act_window(self, name, model):
        action = self.env["ir.actions.act_window"].create(
            {
                "name": name,
                "res_model": model,
                "type": "ir.actions.act_window",
                "view_mode": "list,form",
                "target": "current",
            }
        )
        return action

    def create_tree_view_id(self, model_name):
        view_id = self.env['ir.ui.view'].create(
            {
                "name": model_name + ".list",
                "model": model_name,
                "arch_base": """
                    <list editable='bottom'>
                        <field name="x_name"/>
                    </list>
                """,
            }
        )
        view_id.update_view()
        return view_id

    def create_form_view_id(self, model_name):
        view_id = self.env['ir.ui.view'].create(
            {
                "name": model_name + ".form",
                "model": model_name,
                "arch_base": """
                    <form>
                        <sheet>
                        <group>
                            <field name="x_name"/>
                        </group>
                        </sheet>
                        <chatter/>
                    </form>
                """,
            },
        )

        view_id.update_view()
        return view_id

    def create_search_view_id(self, model_name):
        view_id = self.env['ir.ui.view'].create(
            {
                "name": model_name + ".search",
                "model": model_name,
                "arch_base": """<search><field name="x_name"/></search>""",
            },
        )

        view_id.update_view()
        return view_id
