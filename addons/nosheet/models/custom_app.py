from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os
import unicodedata
import uuid

def dash_text(text):
    text = unicodedata.normalize('NFD', text)
    text = "".join(c for c in text if unicodedata.category(c) != 'Mn')
    text = "_".join(text.split(" "))
    return text.lower().strip()

class CustomApp(models.Model):
    _name = 'nosheet.custom.app'
    _description = 'Custom App'
    _inherit = ['mail.thread']

    _unique_name = models.Constraint(
        'UNIQUE(name)', 
        'This name is already registered!'
    )

    name = fields.Char(string='Name')
    technical_name = fields.Char(string='Technical Name', compute="get_technical_name")
    is_installed = fields.Boolean(string='Is installed', compute="get_is_installed")
    description = fields.Text(string='Description')

    @api.depends('name')
    def get_technical_name(self):
        for record in self:
            if record.name:
                record.technical_name = dash_text(record.name)
            else:
                record.technical_name = False

    @api.depends('name')
    def get_is_installed(self):
        for record in self:
            module = self.env['ir.module.module'].search([
                ('name', '=', record.technical_name), ('author', '!=', "Odoo S.A.")
            ])
            if module:
                record.is_installed = True
            else:
                record.is_installed = False

    uuid = fields.Char(
        string="uuid",
        default=lambda self: f"uuid_{uuid.uuid4().hex}",
        readonly=True,
        required=True,
        copy=False,
    )

    model_ids = fields.One2many(
        'ir.model',
        'from_app_id',
        string='Models'
    )
    menu_id = fields.Many2one(
        'ir.ui.menu',
        string='Menu',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["description"] = vals.get("description") or vals.get("name") or "No Description"

        result =  super(CustomApp, self).create(vals_list)

        for record in result:
            record.create_menu()

        return result

    def create_menu(self):
        menu_id = self.env['ir.ui.menu'].search([('name', '=', self.name), ('parent_id', '=', False), ('is_custom', '=', True)])
        
        if not menu_id:
            menu_id = self.env["ir.ui.menu"].create(
                {
                    "name": self.name,
                    "is_custom": True,
                }
            )
        self.menu_id = menu_id.id

    def uninstall_module(self):
        module = self.env['ir.module.module'].search([
            ('name', '=', self.technical_name), ('author', '!=', "Odoo S.A.")
        ])
        if module:
            return module.button_uninstall_wizard()
        else:
            raise ValidationError("Không tìm thấy module!")

    def unlink(self):
        for record in self:
            record.remove_module()
            record.menu_id.unlink()

        return super(CustomApp, self).unlink()

    def get_folder_path(self):
        current_file = os.path.abspath(__file__)

        models_dir = os.path.dirname(current_file)
        nosheet_dir = os.path.dirname(models_dir)
        addons_dir = os.path.dirname(nosheet_dir)
        new_folder = os.path.join(addons_dir, dash_text(self.name))
        return new_folder

    def create_or_get_manifest(self, new_folder):
        manifest_file_path = os.path.join(new_folder, '__manifest__.py')
        with open(manifest_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""{{
    "name": "{self.description}",
    "version": "1.0",
    "author": "{self.env.user.name}",
    "summary": "{self.description}",
    "depends": ["mail", "base_automation", "nosheet"],
    "application": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}}""")
        return manifest_file_path

    def create_or_get_folder(self):
        new_folder = self.get_folder_path()
        os.makedirs(new_folder, exist_ok=True)
        self.create_or_get_manifest(new_folder)
        return new_folder

    def create_module_py_str(self):
        module_vals = self.read(['name', 'description', 'uuid'])[0]
        module_vals.pop('id', False)
        strs = f'''
from odoo.exceptions import ValidationError
from markupsafe import Markup

def post_init_hook(env):
    custom_module_id = False
    if 'nosheet.custom.app' in env:
        module_vals = {module_vals}
        custom_module_id = env['{self._name}'].create(module_vals)
'''
        return strs

    def create_model_access_right_py_str(self, model_id):
        strs = f'''
        #model access right
'''
        model = self.env['ir.model'].browse(model_id)
        for access in model.access_ids:
            new_vals = access.read(['name', 'perm_read', 'perm_write', 'perm_create', 'perm_unlink'])[0]
            new_vals.pop('id', False)
            strs += f'''
        group_id = False
'''
            group_vals = {}
            privilege_vals = {}
            group_id = access.group_id
            if group_id:
                group_vals = group_id.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                group_vals.pop('id', False)
                if group_id.privilege_id:
                    privilege_vals = group_id.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                    privilege_vals['category_id'] = group_id.privilege_id.category_id.id
                    privilege_vals.pop('id', False)
                strs += f'''
        group_id = env['res.groups'].search([('uuid', '=', '{group_id.uuid}')], limit=1)

        if not group_id:
            group_vals = {group_vals}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group_id.privilege_id.uuid}')], limit=1)
            if {bool(group_id.privilege_id.uuid)} and not privilege_id:
                privilege_vals = {privilege_vals}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)
'''

            strs += f'''
        access_vals = {new_vals}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['{access._name}'].create(access_vals)
'''
        return strs

    def create_model_rules_py_str(self, model_id):
        strs = f'''
        #model rules
'''
        model = self.env['ir.model'].browse(model_id)
        for rule in model.rule_ids:
            new_vals = rule.read(['name', 'domain_force', 'perm_read', 'perm_write', 'perm_create', 'perm_unlink'])[0]
            new_vals.pop('id', False)
            strs += '''
        rule_group_ids = []
'''      
            for group in rule.groups:
                group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                group_vals.pop('id', False)
                privilege_vals = {}
                if group.privilege_id:
                    privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                    privilege_vals['category_id'] = group.privilege_id.category_id.id
                    privilege_vals.pop('id', False)
                strs += f'''
        group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

        if not group_id:
            group_vals = {group_vals}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
            if {bool(group.privilege_id.uuid)} and not privilege_id:
                privilege_vals = {privilege_vals}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        rule_group_ids.append(group_id.id)
'''
            strs += f'''
        rule_vals = {new_vals}
        rule_vals['groups'] = [(6, 0, rule_group_ids)]
        rule_vals['model_id'] = model_id.id
        env['ir.rule'].create(rule_vals)
'''
        return strs

    def create_menus_py_str(self, model_id):
        strs = f'''
        #model menus
'''
        model = self.env['ir.model'].browse(model_id)
        no_action_filters = self.env['ir.filters'].search([('model_id', '=', model.model), ('action_id', '=', False)])
        for filter_ in no_action_filters:
            filter_vals = filter_.read(['name', 'model_id', 'is_default', 'domain', 'context', 'sort'])[0]
            filter_vals.pop('id', False)
            strs += '''
        filter_user_ids = []
'''
            for user in filter_.user_ids:
                strs += f'''
        user_id = env['res.users'].search([('name', '=', '{user.name}')], limit=1)
        if not user_id:
            raise ValidationError('User {user.name} not found, please create it first.')
        else:
            filter_user_ids.append(user_id.id)
'''
            strs += f'''
        filter_vals = {filter_vals}
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)
'''
        actions = self.env["ir.actions.act_window"].search([('res_model', '=', model.model)])
        for action in actions:
            new_action_vals = action.read(['name', 'res_model', 'type', 'usage', 'target', 'cache', 'view_mode', 'mobile_view_mode', 'domain', 'context', 'limit', 'filter', 'help'])[0]
            new_action_vals.pop('id', False)
            action_name = f"ir.actions.act_window,{action.id}"
            menus = self.env['ir.ui.menu'].search([('action', '=', action_name)])
            filters = self.env['ir.filters'].search([('action_id', '=', action.id)])
            strs += '''
        action_group_ids = []
'''          
            for group in action.group_ids:
                group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                group_vals.pop('id', False)
                privilege_vals = {}
                if group.privilege_id:
                    privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                    privilege_vals['category_id'] = group.privilege_id.category_id.id
                    privilege_vals.pop('id', False)
                strs += f'''
        group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

        if not group_id:
            group_vals = {group_vals}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
            if {bool(group.privilege_id.uuid)} and not privilege_id:
                privilege_vals = {privilege_vals}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        action_group_ids.append(group_id.id)
'''
            strs += f'''
        action_vals = {new_action_vals}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)
'''
            for filter_ in filters:
                filter_vals = filter_.read(['name', 'model_id', 'is_default', 'domain', 'context', 'sort'])[0]
                filter_vals.pop('id', False)
                strs += '''
        filter_user_ids = []
'''
                for user in filter_.user_ids:
                    strs += f'''
        user_id = env['res.users'].search([('name', '=', '{user.name}')], limit=1)
        if not user_id:
            raise ValidationError('User {user.name} not found, please create it first.')
        else:
            filter_user_ids.append(user_id.id)
'''
                strs += f'''
        filter_vals = {filter_vals}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)
'''
            for menu in menus: 
                new_menu_vals = menu.read(['name', 'sequence', 'is_custom'])[0]
                new_menu_vals.pop('id', False)
                strs += '''
        menu_group_ids = []
'''
                for group in menu.group_ids:
                    group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                    group_vals.pop('id', False)
                    privilege_vals = {}
                    if group.privilege_id:
                        privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                        privilege_vals['category_id'] = group.privilege_id.category_id.id
                        privilege_vals.pop('id', False)
                    strs += f'''
        group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

        if not group_id:
            group_vals = {group_vals}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
            if {bool(group.privilege_id.uuid)} and not privilege_id:
                privilege_vals = {privilege_vals}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        menu_group_ids.append(group_id.id)
'''
                def recursion_parent_menu(menu):
                    nonlocal strs
                    var_name = f"menu_{menu.id}"
                    var_group_name = f"group_{menu.id}_ids"

                    strs += f'''
        {var_group_name} = []
'''
                    for group in menu.group_ids:
                        group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                        group_vals.pop('id', False)
                        privilege_vals = {}
                        if group.privilege_id:
                            privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                            privilege_vals['category_id'] = group.privilege_id.category_id.id
                            privilege_vals.pop('id', False)
                        strs += f'''
        group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

        if not group_id:
            group_vals = {group_vals}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
            if {bool(group.privilege_id.uuid)} and not privilege_id:
                privilege_vals = {privilege_vals}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        {var_group_name}.append(group_id.id)
'''
                    parent_var = False
                    if menu.parent_id:
                        parent_var = recursion_parent_menu(menu.parent_id)
                    strs += f'''
        menu_domain = [('name', '=', '{menu.name}'), ('is_custom', '=', True)]
        menu_create_domain = {{'name': '{menu.name}', 'sequence': {menu.sequence}, 'group_ids': [(6, 0, {var_group_name})], 'is_custom': True}}
        if {parent_var}:
            menu_domain.append(('parent_id', '=', {parent_var}.id))
            menu_create_domain['parent_id'] = {parent_var}.id
        {var_name} = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not {var_name}:
            {var_name} = env['ir.ui.menu'].create(menu_create_domain)
'''
                    return var_name
                var_name = recursion_parent_menu(menu.parent_id) if menu.parent_id else False
                strs += f'''
        menu_vals = {new_menu_vals}
        menu_vals['action'] = f"ir.actions.act_window,{{action_id.id}}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = {var_name}.id if {var_name} else False
        env['ir.ui.menu'].create(menu_vals)
'''
        return strs
    
    def create_views_py_str(self, model_id):
        strs = f'''
        #model views
'''
        model = self.env['ir.model'].browse(model_id)
        views = self.env["ir.ui.view"].search([('model', '=', model.model)])
        for view in views:
            new_vals = view.read(['name', 'model', 'arch_base', 'mode', 'priority', 'active', 'type'])[0]
            new_vals.pop('id', False)
            strs += f'''
        view_group_ids = []
'''
            for group in view.group_ids:
                group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                group_vals.pop('id', False)
                privilege_vals = {}
                if group.privilege_id:
                    privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                    privilege_vals['category_id'] = group.privilege_id.category_id.id
                    privilege_vals.pop('id', False)
                strs += f'''
        group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

        if not group_id:
            group_vals = {group_vals}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
            if {bool(group.privilege_id.uuid)} and not privilege_id:
                privilege_vals = {privilege_vals}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        view_group_ids.append(group_id.id)
'''
            strs += f'''
        view_vals = {new_vals}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)
'''
        return strs

    def create_models_and_prepare_payloads(self):
        strs = f'''
    fields_payloads = []
    views_payloads = []
    def create_models():
'''
        for model in self.model_ids:
            new_vals = model.read(['name', 'model', 'state', 'transient', 'is_filter_manual', 'is_mail_thread', 'is_mail_activity'])[0]
            new_vals.pop('id', False)
            strs += f'''
        #model {model.name}
        model_vals = {new_vals}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        {self.create_model_access_right_py_str(model.id)}
        {self.create_model_rules_py_str(model.id)}
        {self.create_menus_py_str(model.id)}
        {self.create_views_py_str(model.id)}
'''
            strs += f'''
        #prepare fields for model {model.name}
'''
            for field in model.field_id:
                new_vals = field.read(['name', 'field_description', 'ttype', 'help', 'sequence', 'relation', 'relation_field', 'relation_table', 'column1', 'column2', 'on_delete', 'domain', 'related', 'depends', 'compute', 'required', 'readonly', 'invisible', 'store', 'index', 'copied', 'tracking', 'approval_field'])[0]
                new_vals.pop('id', False)
                strs += f'''
        groups = []
        field_vals = {new_vals}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []
'''
                for selection in field.selection_ids:
                    new_vals = selection.read(['sequence', 'value', 'name'])[0]
                    new_vals.pop('id', False)
                    strs += f'''
        field_vals['selection_vals'].append({new_vals})
'''
                for group in field.groups:
                    group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                    group_vals.pop('id', False)
                    privilege_vals = {}
                    if group.privilege_id:
                        privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                        privilege_vals['category_id'] = group.privilege_id.category_id.id
                        privilege_vals.pop('id', False)
                    strs += f'''
        group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

        if not group_id:
            group_vals = {group_vals}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
            if {bool(group.privilege_id.uuid)} and not privilege_id:
                privilege_vals = {privilege_vals}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)
        groups.append(group_id.id)
'''

                strs += f'''
        field_vals['groups_vals'] = groups
'''
                strs += '''
        fields_payloads.append(field_vals)
'''
        strs += '''
    create_models()
'''
        return strs

    def create_fields(self):
        strs = f'''
    #create fields for all models
    update_fields = []
    fields = sorted(
        fields_payloads,
        key=lambda f: bool(f['related'] or f['depends'] or f['ttype'] == 'one2many' or f['ttype'] == 'many2many')
    )
    for field in fields:
        selection_vals = field.pop('selection_vals', False)
        groups_vals = field.pop('groups_vals', False)
        related = field.pop('related', False)
        depends = field.pop('depends', False)
        compute = field.pop('compute', False)

        if field['relation']:
            t_model = env['ir.model'].search([('model', '=', field['relation'])], limit=1)
            field['selected_model_id'] = t_model.id if t_model else False

            if field['relation_field']:
                t_field = env['ir.model.fields'].search([('model', '=', field['relation']), ('name', '=', field['relation_field'])], limit=1)
                field['selected_field_id'] = t_field.id if t_field else False

        field_id = env['ir.model.fields'].create(field)
        if related or depends or compute:
            update_fields.append({{
                'id': field_id.id,
                'related': related,
                'depends': depends,
                'compute': compute,
            }})
        for selection in selection_vals:
            temp_vals = selection.copy()
            temp_vals['field_id'] = field_id.id
            if field['ttype'] == 'reference':
                t_model = env['ir.model'].search([('model', '=', temp_vals['value'])], limit=1)
                temp_vals['selected_model_id'] = t_model.id if t_model else False
            env['ir.model.fields.selection'].create(temp_vals)
        field_id.groups = [(6, 0, groups_vals)]
    for field in update_fields:
        field_id = env['ir.model.fields'].browse(field['id'])
        field_id.write({{
            'related': field['related'],
            'depends': field['depends'],
            'compute': field['compute'],
        }})
'''
        return strs

    def create_views(self):
        strs = '''
    for view in views_payloads:
        view_id = env['ir.ui.view'].create(view)
        view_id.remove_transient_footer()
        view_id.update_transient_ok_button()
'''
        return strs

    def create_automations(self):
        strs = '''
    #models automation
'''
        for model in self.model_ids:
            autos = self.env['base.automation'].search([('model_id', '=', model.id)])
            strs += f'''
    model_id = env['ir.model'].search([('model', '=', '{model.model}')])
'''
            for auto in autos:
                new_vals = auto.read(['name', 'trigger', 'filter_pre_domain', 'previous_domain', 'filter_domain', 'description'])[0]
                new_vals.pop('id', False)
                strs += f'''
    trigger_field_ids = []
    on_change_field_ids = []
'''
                for trigger in auto.trigger_field_ids:
                    strs += f'''
    field_id = env['ir.model.fields'].search([('model_id', '=', '{model.model}'), ('name', '=', '{trigger.name}')])
    trigger_field_ids.append(field_id.id)
'''
                for on_change in auto.on_change_field_ids:
                    strs += f'''
    field_id = env['ir.model.fields'].search([('model_id', '=', '{model.model}'), ('name', '=', '{on_change.name}')])
    on_change_field_ids.append(field_id.id)
'''
                strs += f'''
    auto_vals = {new_vals}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)
'''
                for action in auto.action_server_ids:
                    new_action_vals = action.read(['name', 'sequence', 'state', 'code', 'evaluation_type', 'update_path', 'value', 'binding_type'])[0]
                    new_action_vals.pop('id', False)
                    strs += '''
    action_group_ids = []
'''
                    for group in action.group_ids:
                        group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                        group_vals.pop('id', False)
                        privilege_vals = {}
                        if group.privilege_id:
                            privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                            privilege_vals['category_id'] = group.privilege_id.category_id.id
                            privilege_vals.pop('id', False)
                        strs += f'''
    group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

    if not group_id:
        group_vals = {group_vals}
        privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
        if {bool(group.privilege_id.uuid)} and not privilege_id:
            privilege_vals = {privilege_vals}
            privilege_id = env['res.groups.privilege'].create(privilege_vals)
        group_vals['privilege_id'] = privilege_id.id if privilege_id else False
        group_id = env['res.groups'].create(group_vals)

    action_group_ids.append(group_id.id)
'''
                    strs += '''
    sequence_id = False
'''
                    if action.sequence_id:
                        new_se_vals = action.sequence_id.read(['name', 'implementation', 'code', 'active', 'prefix', 'suffix', 'padding', 'number_increment', 'use_date_range'])[0]
                        new_se_vals.pop('id', False)
                        strs += f'''
    sequence_id = env['ir.sequence'].create({new_se_vals})
'''
                    strs += f'''
    action_vals = {new_action_vals}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', '{action.update_field_id.name}'), ('model', '=', '{action.update_field_id.model}')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if {bool(action.binding_model_id)}:
        binding_model_id = env['ir.model'].search([('model', '=', '{action.binding_model_id.model}')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)
'''
            action_ids = self.env['ir.actions.server'].search([('model_id', '=', model.id), ('base_automation_id', '=', False)])
            for action in action_ids:
                new_action_vals = action.read(['name', 'sequence', 'state', 'code', 'evaluation_type', 'update_path', 'value', 'binding_type'])[0]
                new_action_vals.pop('id', False)
                strs += '''
    action_group_ids = []
'''
                for group in action.group_ids:
                    group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                    group_vals.pop('id', False)
                    privilege_vals = {}
                    if group.privilege_id:
                        privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                        privilege_vals['category_id'] = group.privilege_id.category_id.id
                        privilege_vals.pop('id', False)
                    strs += f'''
    group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

    if not group_id:
        group_vals = {group_vals}
        privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
        if {bool(group.privilege_id.uuid)} and not privilege_id:
            privilege_vals = {privilege_vals}
            privilege_id = env['res.groups.privilege'].create(privilege_vals)
        group_vals['privilege_id'] = privilege_id.id if privilege_id else False
        group_id = env['res.groups'].create(group_vals)

    action_group_ids.append(group_id.id)
'''
                strs += '''
    sequence_id = False
'''
                if action.sequence_id:
                    new_se_vals = action.sequence_id.read(['name', 'implementation', 'code', 'active', 'prefix', 'suffix', 'padding', 'number_increment', 'use_date_range'])[0]
                    new_se_vals.pop('id', False)
                    strs += f'''
    sequence_id = env['ir.sequence'].create({new_se_vals})
'''
                strs += f'''
    action_vals = {new_action_vals}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', '{action.update_field_id.name}'), ('model', '=', '{action.update_field_id.model}')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if {bool(action.binding_model_id)}:
        binding_model_id = env['ir.model'].search([('model', '=', '{action.binding_model_id.model}')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)
'''
            sche_ids = self.env['ir.cron'].search([('model_id', '=', model.id)])
            for sche in sche_ids:
                new_sche_vals = sche.read(['name', 'interval_number', 'interval_type', 'active', 'priority', 'code'])[0]
                new_sche_vals.pop('id', False)
                strs += '''
    sche_group_ids = []
'''
                for group in sche.group_ids:
                    group_vals = group.read(['name', 'uuid', 'share', 'sequence', 'api_key_duration', 'comment'])[0]
                    group_vals.pop('id', False)
                    privilege_vals = {}
                    if group.privilege_id:
                        privilege_vals = group.privilege_id.read(['name', 'uuid', 'placeholder', 'sequence', 'description'])[0]
                        privilege_vals['category_id'] = group.privilege_id.category_id.id
                        privilege_vals.pop('id', False)
                    strs += f'''
    group_id = env['res.groups'].search([('uuid', '=', '{group.uuid}')], limit=1)

    if not group_id:
        group_vals = {group_vals}
        privilege_id = env['res.groups.privilege'].search([('uuid', '=', '{group.privilege_id.uuid}')], limit=1)
        if {bool(group.privilege_id.uuid)} and not privilege_id:
            privilege_vals = {privilege_vals}
            privilege_id = env['res.groups.privilege'].create(privilege_vals)
        group_vals['privilege_id'] = privilege_id.id if privilege_id else False
        group_id = env['res.groups'].create(group_vals)

    sche_group_ids.append(group_id.id)
'''
                strs += f'''
    sche_vals = {new_sche_vals}
    if {bool(sche.user_id.name)}:
        user_id = env['res.users'].search([('name', '=', '{sche.user_id.name}')], limit=1)
        if not user_id:
            raise ValidationError('User {sche.user_id.name} not found, please create it first.')
        sche_vals['user_id'] = user_id.id
    sche_vals['model_id'] = model_id.id
    sche_vals['group_ids'] = [(6, 0, sche_group_ids)]
    env['ir.cron'].create(sche_vals)
'''
        return strs

    def update_module(self):
        new_folder = self.create_or_get_folder()
        init_file_path = os.path.join(new_folder, '__init__.py')
        with open(init_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""
    {self.create_module_py_str()}
    {self.create_models_and_prepare_payloads()}
    {self.create_fields()}
    {self.create_automations()}
    {self.create_views()}

def uninstall_hook(env):
    rec = env['{self._name}'].search([('uuid', '=', '{self.uuid}')], limit=1)

    if rec:
        rec.unlink()
""")

    def remove_module(self):
        self.model_ids.view_ids.unlink()
        field_ids = self.env['ir.model.fields'].search([('model_id', 'in', self.model_ids.ids), ('state', '=', 'manual')])
        fields = sorted(
            field_ids,
            key=lambda f: bool(f['related'] or f['depends'] or f['ttype'] == 'one2many' or f['ttype'] == 'many2many'),
            reverse=True
        )
        for field in fields:
            field.write({
                "related": False,
                "depends": False,
                "compute": False,
            })
        for field in fields:
            field.unlink()
        for model in self.model_ids:
            model.unlink()
