from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os

class IrModel(models.Model):
    _inherit = ["ir.model", 'mail.thread']

    def _default_field_id(self):
        if self.env.context.get('install_mode'):
            return []                   # no default field when importing
        return [Command.create({'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'copied': True})]

    name = fields.Char(string='Model Description', translate=True, required=True, tracking=True)
    model = fields.Char(
        default=lambda self: f"x_{uuid.uuid4().hex}",
        required=True
    )

    field_id = fields.One2many(
        'ir.model.fields',
        'model_id', string='Fields',
        required=True, copy=True,
        domain=lambda self: self._get_field_id_domain(),
        default=_default_field_id
    )
    is_filter_manual = fields.Boolean(
        string="Is Filter Manual",
        default=True
    )
    from_app_id = fields.Many2one(
        'nosheet.custom.app',
        string='From App',
        tracking=True
    )

    def _get_field_id_domain(self):
        for record in self:
            if record.is_filter_manual:
                return [('state', '=', 'manual')]
            else:
                return []

    server_action_count = fields.Integer(
        compute="_compute_server_action_count"
    )

    view_count = fields.Integer(
        string="Views",
        compute="_compute_view_count"
    )
    base_automation_count = fields.Integer(
        string="Automations",
        compute="_compute_base_automation_count"
    )
    scheduled_action_count = fields.Integer(
        string="Scheduled Actions",
        compute="_compute_scheduled_action_count"
    )
    menu_count = fields.Integer(
        string="Menus",
        compute="_compute_menu_count"
    )

    @api.model_create_multi
    def create(self, vals_list):
        result =  super(IrModel, self).create(vals_list)

        if self.env.context.get('create_views_menu_access'):
            build = self.env['nosheet.build']
            for record in result:
                if record.from_app_id.menu_id:
                    build.add_views_menu_and_access(record.model, record.from_app_id.menu_id.id)

        return result

    def unlink(self):
        build = self.env['nosheet.build']
        for record in self:
            build.clean_up_model(record)

        return super(IrModel, self).unlink()

    def _compute_menu_count(self):
        ActWindow = self.env['ir.actions.act_window']
        Menu = self.env['ir.ui.menu']

        for rec in self:
            actions = ActWindow.search([
                ('res_model', '=', rec.model)
            ])
            if actions:
                action_names = [
                    f"ir.actions.act_window,{a.id}" for a in actions
                ]
                rec.menu_count = Menu.search_count([
                    ('action', 'in', action_names)
                ])
            else:
                rec.menu_count = 0

    def _compute_scheduled_action_count(self):
        Cron = self.env['ir.cron']
        for rec in self:
            rec.scheduled_action_count = Cron.search_count([
                ('model_id', '=', rec.id)
            ])

    def _compute_base_automation_count(self):
        Automation = self.env['base.automation']
        for rec in self:
            rec.base_automation_count = Automation.search_count([
                ('model_id', '=', rec.id)
            ])

    def _compute_view_count(self):
        View = self.env['ir.ui.view']
        for rec in self:
            rec.view_count = View.search_count([
                ('model', '=', rec.model)
            ])

    def _compute_server_action_count(self):
        for rec in self:
            rec.server_action_count = self.env['ir.actions.server'].search_count([
                ('model_id', '=', rec.id)
            ])


    def action_view_server_actions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Server Actions',
            'res_model': 'ir.actions.server',
            'view_mode': 'list,form',
            'domain': [('model_id', '=', self.id)],
            'context': {'default_model_id': self.id},
        }

    def action_view_views(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Views',
            'res_model': 'ir.ui.view',
            'view_mode': 'list,form',
            'domain': [('model', '=', self.model)],
            'context': {'default_model': self.model},
        }

    def action_view_base_automation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Views',
            'res_model': 'base.automation',
            'view_mode': 'list,form',
            'domain': [('model_id', '=', self.id)],
            'context': {'default_model_id': self.id},
        }
    def action_view_scheduled_actions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scheduled Actions',
            'res_model': 'ir.cron',
            'view_mode': 'list,form',
            'domain': [('model_id', '=', self.id)],
            'context': {'default_model_id': self.id},
        }
    def action_view_menus(self):
        self.ensure_one()
        actions = self.env["ir.actions.act_window"].search([('res_model', '=', self.model)])
        action_names = [f"ir.actions.act_window,{a.id}" for a in actions]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Menus',
            'res_model': 'ir.ui.menu',
            'view_mode': 'list,form',
            'domain': [('action', 'in', action_names)],
            'context': {
                'default_action': action_names[0] if action_names else False,
                'default_is_custom': True
            },
        }

    def update_views(self):
        for view in self.view_ids:
            view.update_view()
