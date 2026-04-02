
    
from odoo.exceptions import ValidationError
from markupsafe import Markup

def post_init_hook(env):
    custom_module_id = False
    if 'nosheet.custom.app' in env:
        module_vals = {'name': 'Kế toán', 'description': 'Kế toán', 'uuid': 'uuid_76d79d5175fb48398ee0ba4ee6e11660'}
        custom_module_id = env['nosheet.custom.app'].create(module_vals)

    
    fields_payloads = []
    views_payloads = []
    def create_models():

        #model Công ty
        model_vals = {'name': 'Công ty', 'model': 'x_b5d5cecc141e40a3925a41923922bcc2', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Công ty', 'res_model': 'x_b5d5cecc141e40a3925a41923922bcc2', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Công ty', 'sequence': 4, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_276.id if menu_276 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_b5d5cecc141e40a3925a41923922bcc2.form', 'model': 'x_b5d5cecc141e40a3925a41923922bcc2', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group string="Details">\n            <field name="x_name"/>\n            <field name="x_abbr"/>\n        </group>\n        <notebook>\n            <page string="Accounts">\n                <group>\n                    <group>\n                        <field name="x_tai_khoan_ngan_hang"/>\n                        <field name="x_tai_khoan_tien_mat"/>\n                        <field name="x_tai_khoan_phai_thu"/>\n                        <field name="x_tai_khoan_phai_tra"/>\n                    </group>\n                    <group>\n                        <field name="x_tai_khoan_chi_phi"/>\n                        <field name="x_tai_khoan_doanh_thu"/>\n                        <field name="x_tai_khoan_chiet_khau"/>\n                    </group>\n                </group>\n            </page>\n            <page string="Stock">\n                <group>\n                    <field name="x_tai_khoan_kho"/>\n                    <field name="x_tai_khoan_dieu_chinh"/>\n                    <field name="x_tai_khoan_hn_chua_hd"/>\n                </group>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_b5d5cecc141e40a3925a41923922bcc2.list', 'model': 'x_b5d5cecc141e40a3925a41923922bcc2', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_abbr" optional="show"/>\n    <field name="x_tai_khoan_ngan_hang" optional="show"/>\n    <field name="x_tai_khoan_tien_mat" optional="show"/>\n    <field name="x_tai_khoan_phai_thu" optional="show"/>\n    <field name="x_tai_khoan_phai_tra" optional="show"/>\n    <field name="x_tai_khoan_chi_phi" optional="show"/>\n    <field name="x_tai_khoan_doanh_thu" optional="show"/>\n    <field name="x_tai_khoan_chiet_khau" optional="show"/>\n    <field name="x_tai_khoan_kho" optional="show"/>\n    <field name="x_tai_khoan_dieu_chinh" optional="show"/>\n    <field name="x_tai_khoan_hn_chua_hd" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_b5d5cecc141e40a3925a41923922bcc2.search', 'model': 'x_b5d5cecc141e40a3925a41923922bcc2', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_abbr"/>\n    <field name="x_tai_khoan_ngan_hang"/>\n    <field name="x_tai_khoan_tien_mat"/>\n    <field name="x_tai_khoan_phai_thu"/>\n    <field name="x_tai_khoan_phai_tra"/>\n    <field name="x_tai_khoan_chi_phi"/>\n    <field name="x_tai_khoan_doanh_thu"/>\n    <field name="x_tai_khoan_chiet_khau"/>\n    <field name="x_tai_khoan_kho"/>\n    <field name="x_tai_khoan_dieu_chinh"/>\n    <field name="x_tai_khoan_hn_chua_hd"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Công ty

        groups = []
        field_vals = {'name': 'x_abbr', 'field_description': 'Abbr', 'ttype': 'char', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_chi_phi', 'field_description': 'Tài khoản chi phí', 'ttype': 'many2one', 'help': False, 'sequence': 7, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_chiet_khau', 'field_description': 'Tài khoản chiết khấu', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_dieu_chinh', 'field_description': 'Tài khoản điều chỉnh', 'ttype': 'many2one', 'help': False, 'sequence': 11, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_doanh_thu', 'field_description': 'Tài khoản doanh thu', 'ttype': 'many2one', 'help': False, 'sequence': 8, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_hn_chua_hd', 'field_description': 'Tài khoản HN chưa HĐ', 'ttype': 'many2one', 'help': False, 'sequence': 12, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_kho', 'field_description': 'Tài khoản kho', 'ttype': 'many2one', 'help': False, 'sequence': 10, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_ngan_hang', 'field_description': 'Tài khoản ngân hàng', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_phai_thu', 'field_description': 'Tài khoản phải thu', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_phai_tra', 'field_description': 'Tài khoản phải trả', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_tien_mat', 'field_description': 'Tài khoản tiền mặt', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Danh mục hàng hoá
        model_vals = {'name': 'Danh mục hàng hoá', 'model': 'x_f19155e4689c401ea07a09b90a63f794', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Danh mục hàng hoá', 'res_model': 'x_f19155e4689c401ea07a09b90a63f794', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Danh mục hàng hoá', 'sequence': 1, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_275.id if menu_275 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_f19155e4689c401ea07a09b90a63f794.form', 'model': 'x_f19155e4689c401ea07a09b90a63f794', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_quy_cach"/>\n            <field name="x_dvt"/>\n            <field name="x_gia_ban"/>\n            <field name="x_ghi_chu"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_f19155e4689c401ea07a09b90a63f794.list', 'model': 'x_f19155e4689c401ea07a09b90a63f794', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_quy_cach" optional="show"/>\n    <field name="x_dvt" optional="show"/>\n    <field name="x_gia_ban" optional="show"/>\n    <field name="x_ghi_chu" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_f19155e4689c401ea07a09b90a63f794.search', 'model': 'x_f19155e4689c401ea07a09b90a63f794', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_quy_cach"/>\n    <field name="x_dvt"/>\n    <field name="x_gia_ban"/>\n    <field name="x_ghi_chu"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Danh mục hàng hoá

        groups = []
        field_vals = {'name': 'x_dvt', 'field_description': 'ĐVT', 'ttype': 'selection', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Cái', 'name': 'Cái'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Chiếc', 'name': 'Chiếc'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'text', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_gia_ban', 'field_description': 'Giá bán', 'ttype': 'integer', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_quy_cach', 'field_description': 'Quy cách', 'ttype': 'selection', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': '31x31x31', 'name': '31x31x31'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': '32x32x32', 'name': '32x32x32'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': '33x33x33', 'name': '33x33x33'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Hoá đơn
        model_vals = {'name': 'Hoá đơn', 'model': 'x_8d898fdcdadf451f844fa3ba69f9c226', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Hoá đơn', 'res_model': 'x_8d898fdcdadf451f844fa3ba69f9c226', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_279_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giấy tờ'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giấy tờ', 'sequence': 8, 'group_ids': [(6, 0, group_279_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_279 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_279:
            menu_279 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Hoá đơn', 'sequence': 4, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_279.id if menu_279 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_8d898fdcdadf451f844fa3ba69f9c226.form', 'model': 'x_8d898fdcdadf451f844fa3ba69f9c226', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_8d898fdcdadf451f844fa3ba69f9c226.list', 'model': 'x_8d898fdcdadf451f844fa3ba69f9c226', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_8d898fdcdadf451f844fa3ba69f9c226.search', 'model': 'x_8d898fdcdadf451f844fa3ba69f9c226', 'arch_base': '<search>\n    <field name="x_name"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Hoá đơn

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Hợp đồng
        model_vals = {'name': 'Hợp đồng', 'model': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Hợp đồng', 'res_model': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_279_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giấy tờ'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giấy tờ', 'sequence': 8, 'group_ids': [(6, 0, group_279_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_279 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_279:
            menu_279 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Hợp đồng', 'sequence': 1, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_279.id if menu_279 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_5579eb7c8c8f454cb54cd8e85234d153.form', 'model': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_doi_tac"/>\n            <field name="x_cong_ty"/>\n        </group>\n        <notebook>\n            <page string="Items" name="x_items" invisible="context.get(\'hide_items\')">\n                <field name="x_items">\n                    <list editable="bottom">\n                        <field name="x_name" optional="show"/>\n                        <field name="x_ngay_thang" optional="hide"/>\n                        <field name="x_so_hd" optional="hide"/>\n                        <field name="x_doi_tac" optional="hide"/>\n                        <field name="x_kho_hang" optional="show"/>\n                        <field name="x_hang_hoa" optional="show"/>\n                        <field name="x_muc_dich" optional="show"/>\n                        <field name="x_so_luong" optional="show"/>\n                        <field name="x_don_gia" optional="show"/>\n                        <field name="x_thanh_tien" optional="show" sum="Thành tiền"/>\n                        <field name="x_thanh_toan" optional="show" sum="Thanh toán"/>\n                        <field name="x_cong_ty" optional="hide"/>\n                        <field name="x_gia_von" optional="show"/>\n                        <field name="x_nhat_ky_thanh_toan" widget="many2many_tags" optional="hide"/>\n                    </list>\n                </field>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_5579eb7c8c8f454cb54cd8e85234d153.list', 'model': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_doi_tac" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_5579eb7c8c8f454cb54cd8e85234d153.search', 'model': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_doi_tac"/>\n    <field name="x_cong_ty"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Hợp đồng

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_doi_tac', 'field_description': 'Đối tác', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Items', 'ttype': 'one2many', 'help': False, 'sequence': 5, 'relation': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'relation_field': 'x_so_hd', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Kho hàng
        model_vals = {'name': 'Kho hàng', 'model': 'x_a6da8efa11194f1bae3b7522c10e954b', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Kho hàng', 'res_model': 'x_a6da8efa11194f1bae3b7522c10e954b', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Kho hàng', 'sequence': 5, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_276.id if menu_276 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_a6da8efa11194f1bae3b7522c10e954b.form', 'model': 'x_a6da8efa11194f1bae3b7522c10e954b', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_a6da8efa11194f1bae3b7522c10e954b.list', 'model': 'x_a6da8efa11194f1bae3b7522c10e954b', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_a6da8efa11194f1bae3b7522c10e954b.search', 'model': 'x_a6da8efa11194f1bae3b7522c10e954b', 'arch_base': '<search>\n    <field name="x_name"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Kho hàng

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Mua bán hàng hoá
        model_vals = {'name': 'Mua bán hàng hoá', 'model': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Mua bán hàng hoá', 'res_model': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Mua bán hàng hoá', 'sequence': 2, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_275.id if menu_275 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8.form', 'model': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_so_hd"/>\n            <field name="x_doi_tac"/>\n            <field name="x_hang_hoa"/>\n            <field name="x_muc_dich"/>\n            <field name="x_so_luong"/>\n            <field name="x_don_gia"/>\n            <field name="x_thanh_tien"/>\n            <field name="x_thanh_toan"/>\n            <field name="x_kho_hang"/>\n            <field name="x_cong_ty"/>\n            <field name="x_gia_von"/>\n        </group>\n        <notebook>\n            <page string="Nhật ký thanh toán" name="x_nhat_ky_thanh_toan">\n                <field name="x_nhat_ky_thanh_toan"/>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8.list', 'model': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_so_hd" optional="show" context="{\'hide_items\': True}"/>\n    <field name="x_doi_tac" optional="show"/>\n    <field name="x_kho_hang" optional="show"/>\n    <field name="x_hang_hoa" optional="show"/>\n    <field name="x_muc_dich" optional="show"/>\n    <field name="x_so_luong" optional="show"/>\n    <field name="x_don_gia" optional="show"/>\n    <field name="x_thanh_tien" optional="show"/>\n    <field name="x_thanh_toan" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n    <field name="x_gia_von" optional="show"/>\n    <field name="x_nhat_ky_thanh_toan" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8.search', 'model': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_so_hd"/>\n    <field name="x_doi_tac"/>\n    <field name="x_hang_hoa"/>\n    <field name="x_muc_dich"/>\n    <field name="x_so_luong"/>\n    <field name="x_don_gia"/>\n    <field name="x_thanh_tien"/>\n    <field name="x_thanh_toan"/>\n    <field name="x_kho_hang"/>\n    <field name="x_cong_ty"/>\n    <field name="x_gia_von"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Mua bán hàng hoá

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 14, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_so_hd.x_cong_ty', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_doi_tac', 'field_description': 'Đối tác', 'ttype': 'many2one', 'help': False, 'sequence': 4, 'relation': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_so_hd.x_doi_tac', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_don_gia', 'field_description': 'Đơn giá', 'ttype': 'float', 'help': False, 'sequence': 11, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_gia_von', 'field_description': 'Giá vốn', 'ttype': 'float', 'help': False, 'sequence': 15, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa', 'field_description': 'Hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_f19155e4689c401ea07a09b90a63f794', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_hang', 'field_description': 'Kho hàng', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_a6da8efa11194f1bae3b7522c10e954b', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_muc_dich', 'field_description': 'Mục đích', 'ttype': 'selection', 'help': False, 'sequence': 9, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Nhập', 'name': 'Mua hàng'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Xuất', 'name': 'Bán hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_so_hd.x_ngay_thang', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_nhat_ky_thanh_toan', 'field_description': 'Nhật ký thanh toán', 'ttype': 'one2many', 'help': False, 'sequence': 16, 'relation': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'relation_field': 'x_mua_ban_hang_hoa', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_so_hd', 'field_description': 'Số HĐ', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_so_luong', 'field_description': 'Số lượng', 'ttype': 'integer', 'help': False, 'sequence': 10, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_thanh_tien', 'field_description': 'Thành tiền', 'ttype': 'float', 'help': False, 'sequence': 12, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': 'x_so_luong, x_don_gia', 'compute': 'PRODUCT("x_so_luong:x_don_gia")', 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_thanh_toan', 'field_description': 'Thanh toán', 'ttype': 'float', 'help': False, 'sequence': 13, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': 'x_nhat_ky_thanh_toan', 'compute': 'SUM_COL("x_thanh_toan", "x_nhat_ky_thanh_toan")', 'required': False, 'readonly': True, 'invisible': False, 'store': False, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Nghiệp vụ khác
        model_vals = {'name': 'Nghiệp vụ khác', 'model': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Nghiệp vụ khác', 'res_model': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Nghiệp vụ khác', 'sequence': 4, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_275.id if menu_275 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_4b01b3eb8ec04fff8d7a74437491f315.form', 'model': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_cong_ty"/>\n            <field name="x_ghi_chu"/>\n        </group>\n        <notebook>\n            <page string="Items" name="x_items">\n                <field name="x_items">\n                    <list editable="bottom">\n                        <field name="x_name" optional="show"/>\n                        <field name="x_ngay_thang" optional="show" readonly="1"/>\n                        <field name="x_tai_khoan" optional="show"/>\n                        <field name="x_debit" optional="show"/>\n                        <field name="x_credit" optional="show"/>\n                        <field name="x_balance" optional="hide"/>\n                        <field name="x_loai_chung_tu" optional="hide"/>\n                        <field name="x_tai_khoan_doi_ung" optional="hide"/>\n                        <field name="x_doi_tac" optional="hide"/>\n                        <field name="x_cong_ty" optional="hide"/>\n                        <field name="x_parent_account" optional="hide"/>\n                        <field name="x_root_type" optional="hide"/>\n                        <field name="x_report_type" optional="hide"/>\n                        <field name="x_account_type" optional="hide"/>\n                        <field name="x_ghi_chu" optional="show"/>\n                        <field name="x_nghiep_vu_khac" optional="hide"/>\n                    </list>\n                </field>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_4b01b3eb8ec04fff8d7a74437491f315.list', 'model': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n    <field name="x_ghi_chu" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_4b01b3eb8ec04fff8d7a74437491f315.search', 'model': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_cong_ty"/>\n    <field name="x_ghi_chu"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Nghiệp vụ khác

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'text', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Items', 'ttype': 'one2many', 'help': False, 'sequence': 5, 'relation': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'relation_field': 'x_nghiep_vu_khac', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Nhật ký thanh toán
        model_vals = {'name': 'Nhật ký thanh toán', 'model': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Nhật ký thanh toán', 'res_model': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_279_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giấy tờ'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giấy tờ', 'sequence': 8, 'group_ids': [(6, 0, group_279_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_279 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_279:
            menu_279 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Nhật ký thanh toán', 'sequence': 5, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_279.id if menu_279 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_0cb7fa70192b4a6eab9403509aa45ca0.form', 'model': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_loai_thanh_toan"/>\n            <field name="x_thanh_toan"/>\n            <field name="x_mua_ban_hang_hoa"/>\n            <field name="x_hoa_don"/>\n            <field name="x_cong_ty"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_0cb7fa70192b4a6eab9403509aa45ca0.list', 'model': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_loai_thanh_toan" optional="show"/>\n    <field name="x_thanh_toan" optional="show"/>\n    <field name="x_mua_ban_hang_hoa" optional="show"/>\n    <field name="x_hoa_don" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_0cb7fa70192b4a6eab9403509aa45ca0.search', 'model': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_loai_thanh_toan"/>\n    <field name="x_thanh_toan"/>\n    <field name="x_mua_ban_hang_hoa"/>\n    <field name="x_hoa_don"/>\n    <field name="x_cong_ty"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Nhật ký thanh toán

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 7, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_mua_ban_hang_hoa.x_cong_ty', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hoa_don', 'field_description': 'Hoá đơn', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_8d898fdcdadf451f844fa3ba69f9c226', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_thanh_toan', 'field_description': 'Loại thanh toán', 'ttype': 'selection', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Tiền mặt', 'name': 'Tiền mặt'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Ngân hàng', 'name': 'Ngân hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_mua_ban_hang_hoa', 'field_description': 'Mua bán hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_thanh_toan', 'field_description': 'Thanh toán', 'ttype': 'float', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Phiếu kho
        model_vals = {'name': 'Phiếu kho', 'model': 'x_2d75d5f44f924a9282735b054b0007a1', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Phiếu kho', 'res_model': 'x_2d75d5f44f924a9282735b054b0007a1', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_279_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giấy tờ'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giấy tờ', 'sequence': 8, 'group_ids': [(6, 0, group_279_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_279 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_279:
            menu_279 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Phiếu kho', 'sequence': 3, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_279.id if menu_279 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_2d75d5f44f924a9282735b054b0007a1.form', 'model': 'x_2d75d5f44f924a9282735b054b0007a1', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_kho_nguon"/>\n            <field name="x_kho_dich"/>\n            <field name="x_cong_ty"/>\n        </group>\n        <notebook>\n            <page string="Items" name="x_items" invisible="context.get(\'hide_items\')">\n                <field name="x_items">\n                    <list editable="bottom">\n                        <field name="x_name" optional="show"/>\n                        <field name="x_ngay_thang" optional="hide"/>\n                        <field name="x_phieu_kho" optional="hide"/>\n                        <field name="x_muc_dich" optional="show"/>\n                        <field name="x_kho_nguon" optional="hide"/>\n                        <field name="x_kho_dich" optional="hide"/>\n                        <field name="x_hang_hoa" optional="show"/>\n                        <field name="x_so_luong" optional="show"/>\n                        <field name="x_gia_tri" optional="show" sum="giá trị"/>\n                        <field name="x_cong_ty" optional="hide"/>\n                    </list>\n                </field>\n            </page>\n        </notebook>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_2d75d5f44f924a9282735b054b0007a1.list', 'model': 'x_2d75d5f44f924a9282735b054b0007a1', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_kho_nguon" optional="show"/>\n    <field name="x_kho_dich" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n    <field name="x_items" widget="many2many_tags" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_2d75d5f44f924a9282735b054b0007a1.search', 'model': 'x_2d75d5f44f924a9282735b054b0007a1', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_kho_nguon"/>\n    <field name="x_kho_dich"/>\n    <field name="x_cong_ty"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Phiếu kho

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_items', 'field_description': 'Items', 'ttype': 'one2many', 'help': False, 'sequence': 7, 'relation': 'x_1252b666e8a04a17930b0c4166d12b43', 'relation_field': 'x_phieu_kho', 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_dich', 'field_description': 'Kho đích', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_a6da8efa11194f1bae3b7522c10e954b', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_nguon', 'field_description': 'Kho nguồn', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_a6da8efa11194f1bae3b7522c10e954b', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Sổ cái kho
        model_vals = {'name': 'Sổ cái kho', 'model': 'x_c78095f0ddb645eca0cd38dee357725c', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Báo cáo hàng hoá', 'res_model': 'x_c78095f0ddb645eca0cd38dee357725c', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'pivot', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        filter_user_ids = []

        filter_vals = {'name': 'Báo cáo hàng hoá', 'model_id': 'x_c78095f0ddb645eca0cd38dee357725c', 'is_default': True, 'domain': '[("x_loai_ky", "!=", False)]', 'context': "{'group_by': [], 'pivot_measures': ['x_so_luong', 'x_tong_gia_tri'], 'pivot_column_groupby': ['x_loai_ky', 'x_kho_hang'], 'pivot_row_groupby': ['x_hang_hoa']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        menu_group_ids = []

        group_287_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Báo cáo'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Báo cáo', 'sequence': 7, 'group_ids': [(6, 0, group_287_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_287 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_287:
            menu_287 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Báo cáo hàng hoá', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_287.id if menu_287 else False
        env['ir.ui.menu'].create(menu_vals)

        action_group_ids = []

        action_vals = {'name': 'Sổ cái kho', 'res_model': 'x_c78095f0ddb645eca0cd38dee357725c', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_289_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Sổ cái'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Sổ cái', 'sequence': 9, 'group_ids': [(6, 0, group_289_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_289 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_289:
            menu_289 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Sổ cái kho', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_289.id if menu_289 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'pivot', 'model': 'x_c78095f0ddb645eca0cd38dee357725c', 'arch_base': '<pivot>\n    <field name="x_loai_ky" type="col"/>\n    <field name="x_kho_hang" type="col"/>\n    <field name="x_hang_hoa" type="row"/>\n    <field name="x_so_luong" type="measure"/>\n    <field name="x_tong_gia_tri" type="measure"/>\n    <field name="x_muc_dich"/>\n</pivot>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'pivot'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c78095f0ddb645eca0cd38dee357725c.form', 'model': 'x_c78095f0ddb645eca0cd38dee357725c', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_so_luong"/>\n            <field name="x_gia_von"/>\n            <field name="x_tong_gia_tri"/>\n            <field name="x_muc_dich"/>\n            <field name="x_loai_chung_tu"/>\n            <field name="x_hang_hoa"/>\n            <field name="x_kho_hang"/>\n            <field name="x_cong_ty"/>\n            <field name="x_loai_ky"/>\n            <field name="x_ghi_chu"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c78095f0ddb645eca0cd38dee357725c.list', 'model': 'x_c78095f0ddb645eca0cd38dee357725c', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_so_luong" optional="show"/>\n    <field name="x_gia_von" optional="show"/>\n    <field name="x_tong_gia_tri" optional="show"/>\n    <field name="x_muc_dich" optional="show"/>\n    <field name="x_loai_chung_tu" optional="show"/>\n    <field name="x_hang_hoa" optional="show"/>\n    <field name="x_kho_hang" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n    <field name="x_loai_ky" optional="show"/>\n    <field name="x_ghi_chu" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_c78095f0ddb645eca0cd38dee357725c.search', 'model': 'x_c78095f0ddb645eca0cd38dee357725c', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_so_luong"/>\n    <field name="x_gia_von"/>\n    <field name="x_tong_gia_tri"/>\n    <field name="x_muc_dich"/>\n    <field name="x_loai_chung_tu"/>\n    <field name="x_hang_hoa"/>\n    <field name="x_kho_hang"/>\n    <field name="x_cong_ty"/>\n    <field name="x_loai_ky"/>\n    <field name="x_ghi_chu"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Sổ cái kho

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 10, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'text', 'help': False, 'sequence': 12, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_gia_von', 'field_description': 'Giá vốn', 'ttype': 'float', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa', 'field_description': 'Hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 8, 'relation': 'x_f19155e4689c401ea07a09b90a63f794', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_hang', 'field_description': 'Kho hàng', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_a6da8efa11194f1bae3b7522c10e954b', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_chung_tu', 'field_description': 'Loại chứng từ', 'ttype': 'reference', 'help': False, 'sequence': 7, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'x_1252b666e8a04a17930b0c4166d12b43', 'name': 'Xuất nhập kho'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'name': 'Mua bán hàng hoá'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_ky', 'field_description': 'Loại kỳ', 'ttype': 'selection', 'help': False, 'sequence': 11, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Tồn đầu kỳ', 'name': 'Tồn đầu kỳ'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Nhập trong kỳ', 'name': 'Nhập trong kỳ'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'Xuất bán trong kỳ', 'name': 'Xuất bán trong kỳ'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_muc_dich', 'field_description': 'Mục đích', 'ttype': 'selection', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Xuất', 'name': 'Xuất'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Nhập', 'name': 'Nhập'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_so_luong', 'field_description': 'Số lượng', 'ttype': 'float', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tong_gia_tri', 'field_description': 'Tổng giá trị', 'ttype': 'float', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': 'x_so_luong, x_gia_von', 'compute': 'PRODUCT("x_so_luong:x_gia_von")', 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Sổ cái kế toán
        model_vals = {'name': 'Sổ cái kế toán', 'model': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Báo cáo tổng hợp', 'res_model': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'pivot', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        filter_user_ids = []

        filter_vals = {'name': 'Balance Sheet', 'model_id': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'is_default': False, 'domain': '[("x_report_type", "=", "Balance Sheet")]', 'context': "{'group_by': [], 'pivot_measures': ['x_balance'], 'pivot_column_groupby': [], 'pivot_row_groupby': ['x_tai_khoan']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        filter_user_ids = []

        filter_vals = {'name': 'Profit and Loss', 'model_id': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'is_default': False, 'domain': '[("x_report_type", "=", "Profit and Loss")]', 'context': "{'group_by': [], 'pivot_measures': ['x_balance'], 'pivot_column_groupby': [], 'pivot_row_groupby': ['x_tai_khoan']}", 'sort': '[]'}
        filter_vals['action_id'] = action_id.id if action_id else False
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        menu_group_ids = []

        group_287_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Báo cáo'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Báo cáo', 'sequence': 7, 'group_ids': [(6, 0, group_287_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_287 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_287:
            menu_287 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Báo cáo tổng hợp', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_287.id if menu_287 else False
        env['ir.ui.menu'].create(menu_vals)

        action_group_ids = []

        action_vals = {'name': 'Sổ cái kế toán', 'res_model': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_289_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Sổ cái'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Sổ cái', 'sequence': 9, 'group_ids': [(6, 0, group_289_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_289 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_289:
            menu_289 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Sổ cái kế toán', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_289.id if menu_289 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'pivot', 'model': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'arch_base': '<pivot>\n    <field name="x_tai_khoan" type="row"/>\n    <!--<field name="x_debit" type="measure"/>-->\n    <!--<field name="x_credit" type="measure"/>-->\n    <field name="x_balance" type="measure"/>\n</pivot>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'pivot'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_e4a49df8fa1c4db9a0d729719332b9eb.form', 'model': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_tai_khoan"/>\n            <field name="x_debit"/>\n            <field name="x_credit"/>\n            <field name="x_balance"/>\n            <field name="x_loai_chung_tu"/>\n            <field name="x_tai_khoan_doi_ung"/>\n            <field name="x_doi_tac"/>\n            <field name="x_cong_ty"/>\n            <field name="x_parent_account"/>\n            <field name="x_root_type"/>\n            <field name="x_report_type"/>\n            <field name="x_account_type"/>\n            <field name="x_ghi_chu"/>\n            <field name="x_nghiep_vu_khac"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_e4a49df8fa1c4db9a0d729719332b9eb.list', 'model': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_tai_khoan" optional="show"/>\n    <field name="x_debit" optional="show"/>\n    <field name="x_credit" optional="show"/>\n    <field name="x_balance" optional="show"/>\n    <field name="x_loai_chung_tu" optional="show"/>\n    <field name="x_tai_khoan_doi_ung" optional="show"/>\n    <field name="x_doi_tac" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n    <field name="x_parent_account" optional="show"/>\n    <field name="x_root_type" optional="show"/>\n    <field name="x_report_type" optional="show"/>\n    <field name="x_account_type" optional="show"/>\n    <field name="x_ghi_chu" optional="show"/>\n    <field name="x_nghiep_vu_khac" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_e4a49df8fa1c4db9a0d729719332b9eb.search', 'model': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_tai_khoan"/>\n    <field name="x_debit"/>\n    <field name="x_credit"/>\n    <field name="x_balance"/>\n    <field name="x_loai_chung_tu"/>\n    <field name="x_tai_khoan_doi_ung"/>\n    <field name="x_doi_tac"/>\n    <field name="x_cong_ty"/>\n    <field name="x_parent_account"/>\n    <field name="x_root_type"/>\n    <field name="x_report_type"/>\n    <field name="x_account_type"/>\n    <field name="x_ghi_chu"/>\n    <field name="x_nghiep_vu_khac"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Sổ cái kế toán

        groups = []
        field_vals = {'name': 'x_account_type', 'field_description': 'Account Type', 'ttype': 'selection', 'help': False, 'sequence': 15, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_tai_khoan.x_account_type', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_balance', 'field_description': 'Balance', 'ttype': 'float', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': 'x_credit, x_debit', 'compute': 'MINUS("x_credit:x_debit")', 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 11, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_credit', 'field_description': 'Credit', 'ttype': 'float', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_debit', 'field_description': 'Debit', 'ttype': 'float', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_doi_tac', 'field_description': 'Đối tác', 'ttype': 'many2one', 'help': False, 'sequence': 10, 'relation': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ghi_chu', 'field_description': 'Ghi chú', 'ttype': 'char', 'help': False, 'sequence': 16, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_chung_tu', 'field_description': 'Loại chứng từ', 'ttype': 'reference', 'help': False, 'sequence': 8, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'name': 'Nhật ký thanh toán'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'x_2d75d5f44f924a9282735b054b0007a1', 'name': 'Phiếu kho'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'name': 'Hợp đồng'})

        field_vals['selection_vals'].append({'sequence': 3, 'value': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'name': 'Nghiệp vụ khác'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_nghiep_vu_khac', 'field_description': 'Nghiệp vụ khác', 'ttype': 'many2one', 'help': False, 'sequence': 17, 'relation': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_parent_account', 'field_description': 'Parent Account', 'ttype': 'many2one', 'help': False, 'sequence': 12, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_tai_khoan.x_parent_account', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_report_type', 'field_description': 'Report Type', 'ttype': 'selection', 'help': False, 'sequence': 14, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_tai_khoan.x_report_type', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_root_type', 'field_description': 'Root Type', 'ttype': 'selection', 'help': False, 'sequence': 13, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_tai_khoan.x_root_type', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan', 'field_description': 'Tài khoản', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': "[('x_is_group', '=', False)]", 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tai_khoan_doi_ung', 'field_description': 'Tài khoản đối ứng', 'ttype': 'char', 'help': False, 'sequence': 9, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Tài khoản
        model_vals = {'name': 'Tài khoản', 'model': 'x_6fc605916fea47c3bbd6da0a25660665', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        filter_user_ids = []

        filter_vals = {'name': 'account', 'model_id': 'x_6fc605916fea47c3bbd6da0a25660665', 'is_default': True, 'domain': '[("x_is_group", "=", False)]', 'context': "{'group_by': []}", 'sort': '[]'}
        filter_vals['user_ids'] = [(6, 0, filter_user_ids)]
        env['ir.filters'].create(filter_vals)

        action_group_ids = []

        action_vals = {'name': 'Tài khoản', 'res_model': 'x_6fc605916fea47c3bbd6da0a25660665', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Tài khoản', 'sequence': 6, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_276.id if menu_276 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_6fc605916fea47c3bbd6da0a25660665.form', 'model': 'x_6fc605916fea47c3bbd6da0a25660665', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <group>\n                <field name="x_is_group"/>\n                <field name="x_name"/>\n                <field name="x_account_number"/>\n                <field name="x_company"/>\n                <field name="x_root_type"/>\n                <field name="x_report_type"/>\n            </group>\n            <group>\n                <field name="x_parent_account"/>\n                <field name="x_account_type"/>\n                <field name="x_balance_must_be"/>\n            </group>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_6fc605916fea47c3bbd6da0a25660665.list', 'model': 'x_6fc605916fea47c3bbd6da0a25660665', 'arch_base': '<list>\n    <field name="x_name" optional="show"/>\n    <field name="x_is_group" optional="show"/>\n    <field name="x_parent_account" optional="show"/>\n    <field name="x_account_number" optional="show"/>\n    <field name="x_root_type" optional="show"/>\n    <field name="x_report_type" optional="show"/>\n    <field name="x_account_type" optional="show"/>\n    <field name="x_balance_must_be" optional="show"/>\n    <field name="x_company" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_6fc605916fea47c3bbd6da0a25660665.search', 'model': 'x_6fc605916fea47c3bbd6da0a25660665', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_is_group"/>\n    <field name="x_parent_account"/>\n    <field name="x_account_number"/>\n    <field name="x_root_type"/>\n    <field name="x_report_type"/>\n    <field name="x_account_type"/>\n    <field name="x_balance_must_be"/>\n    <field name="x_company"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Tài khoản

        groups = []
        field_vals = {'name': 'x_account_number', 'field_description': 'Account Number', 'ttype': 'integer', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_account_type', 'field_description': 'Account Type', 'ttype': 'selection', 'help': False, 'sequence': 7, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Stock', 'name': 'Stock'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Stock Received But Not Billed', 'name': 'Stock Received But Not Billed'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'Cost of Goods Sold', 'name': 'Cost of Goods Sold'})

        field_vals['selection_vals'].append({'sequence': 3, 'value': 'Stock Adjustment', 'name': 'Stock Adjustment'})

        field_vals['selection_vals'].append({'sequence': 4, 'value': 'Payable', 'name': 'Payable'})

        field_vals['selection_vals'].append({'sequence': 5, 'value': 'Receivable', 'name': 'Receivable'})

        field_vals['selection_vals'].append({'sequence': 6, 'value': 'Cash', 'name': 'Cash'})

        field_vals['selection_vals'].append({'sequence': 7, 'value': 'Bank', 'name': 'Bank'})

        field_vals['selection_vals'].append({'sequence': 8, 'value': 'Equity', 'name': 'Equity'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_balance_must_be', 'field_description': 'Balance must be', 'ttype': 'selection', 'help': False, 'sequence': 8, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Debit', 'name': 'Debit'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Credit', 'name': 'Credit'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_company', 'field_description': 'Company', 'ttype': 'many2one', 'help': False, 'sequence': 9, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_is_group', 'field_description': 'Is group', 'ttype': 'boolean', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_parent_account', 'field_description': 'Parent Account', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_6fc605916fea47c3bbd6da0a25660665', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_report_type', 'field_description': 'Report Type', 'ttype': 'selection', 'help': False, 'sequence': 6, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Balance Sheet', 'name': 'Balance Sheet'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Profit and Loss', 'name': 'Profit and Loss'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_root_type', 'field_description': 'Root Type', 'ttype': 'selection', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Asset', 'name': 'Asset'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Liability', 'name': 'Liability'})

        field_vals['selection_vals'].append({'sequence': 2, 'value': 'Income', 'name': 'Income'})

        field_vals['selection_vals'].append({'sequence': 3, 'value': 'Expense', 'name': 'Expense'})

        field_vals['selection_vals'].append({'sequence': 4, 'value': 'Equity', 'name': 'Equity'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Xuất nhập kho
        model_vals = {'name': 'Xuất nhập kho', 'model': 'x_1252b666e8a04a17930b0c4166d12b43', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Xuất nhập kho', 'res_model': 'x_1252b666e8a04a17930b0c4166d12b43', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Xuất nhập kho', 'sequence': 3, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_275.id if menu_275 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_1252b666e8a04a17930b0c4166d12b43.form', 'model': 'x_1252b666e8a04a17930b0c4166d12b43', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_phieu_kho"/>\n            <field name="x_muc_dich"/>\n            <field name="x_kho_nguon"/>\n            <field name="x_kho_dich"/>\n            <field name="x_hang_hoa"/>\n            <field name="x_so_luong"/>\n            <field name="x_gia_tri"/>\n            <field name="x_cong_ty"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_1252b666e8a04a17930b0c4166d12b43.list', 'model': 'x_1252b666e8a04a17930b0c4166d12b43', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_phieu_kho" optional="show" context="{\'hide_items\': True}"/>\n    <field name="x_muc_dich" optional="show"/>\n    <field name="x_kho_nguon" optional="show"/>\n    <field name="x_kho_dich" optional="show"/>\n    <field name="x_hang_hoa" optional="show"/>\n    <field name="x_so_luong" optional="show"/>\n    <field name="x_gia_tri" optional="show"/>\n    <field name="x_cong_ty" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_1252b666e8a04a17930b0c4166d12b43.search', 'model': 'x_1252b666e8a04a17930b0c4166d12b43', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_phieu_kho"/>\n    <field name="x_muc_dich"/>\n    <field name="x_kho_nguon"/>\n    <field name="x_kho_dich"/>\n    <field name="x_hang_hoa"/>\n    <field name="x_so_luong"/>\n    <field name="x_gia_tri"/>\n    <field name="x_cong_ty"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Xuất nhập kho

        groups = []
        field_vals = {'name': 'x_cong_ty', 'field_description': 'Công ty', 'ttype': 'many2one', 'help': False, 'sequence': 10, 'relation': 'x_b5d5cecc141e40a3925a41923922bcc2', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_phieu_kho.x_cong_ty', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_gia_tri', 'field_description': 'Giá trị', 'ttype': 'float', 'help': False, 'sequence': 9, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hang_hoa', 'field_description': 'Hàng hoá', 'ttype': 'many2one', 'help': False, 'sequence': 7, 'relation': 'x_f19155e4689c401ea07a09b90a63f794', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_dich', 'field_description': 'Kho đích', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_a6da8efa11194f1bae3b7522c10e954b', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': 'x_phieu_kho.x_kho_dich', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_kho_nguon', 'field_description': 'Kho nguồn', 'ttype': 'many2one', 'help': False, 'sequence': 5, 'relation': 'x_a6da8efa11194f1bae3b7522c10e954b', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': 'x_phieu_kho, x_muc_dich', 'compute': 'SET(lambda e: e.x_phieu_kho.x_kho_nguon if e.x_muc_dich == "Xuất" else False)', 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_muc_dich', 'field_description': 'Mục đích', 'ttype': 'selection', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Nhập', 'name': 'Nhập kho'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Xuất', 'name': 'Xuất kho'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': 'x_phieu_kho.x_ngay_thang', 'depends': False, 'compute': False, 'required': False, 'readonly': True, 'invisible': False, 'store': True, 'index': False, 'copied': False, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_phieu_kho', 'field_description': 'Phiếu kho', 'ttype': 'many2one', 'help': False, 'sequence': 3, 'relation': 'x_2d75d5f44f924a9282735b054b0007a1', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_so_luong', 'field_description': 'Số lượng', 'ttype': 'integer', 'help': False, 'sequence': 8, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Đối tác
        model_vals = {'name': 'Đối tác', 'model': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'state': 'manual', 'transient': False, 'is_filter_manual': True, 'is_mail_thread': True, 'is_mail_activity': True}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Đối tác', 'res_model': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': Markup('<p class="o_view_nocontent_smiling_face">Create new document</p>')}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_279_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Giấy tờ'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Giấy tờ', 'sequence': 8, 'group_ids': [(6, 0, group_279_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_279 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_279:
            menu_279 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Đối tác', 'sequence': 2, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_279.id if menu_279 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_00c5b25ba4f54ad085e01b57b20eb8a9.form', 'model': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name"/>\n        </group>\n        <notebook/>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_00c5b25ba4f54ad085e01b57b20eb8a9.list', 'model': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_00c5b25ba4f54ad085e01b57b20eb8a9.search', 'model': 'x_00c5b25ba4f54ad085e01b57b20eb8a9', 'arch_base': '<search>\n    <field name="x_name"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Đối tác

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Form báo cáo kho
        model_vals = {'name': 'Form báo cáo kho', 'model': 'x_176bc4d70e5c4c4cb919046b1475cec6', 'state': 'manual', 'transient': True, 'is_filter_manual': True, 'is_mail_thread': False, 'is_mail_activity': False}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Form báo cáo kho', 'res_model': 'x_176bc4d70e5c4c4cb919046b1475cec6', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': False}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_296_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Popup'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Popup', 'sequence': 10, 'group_ids': [(6, 0, group_296_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_296 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_296:
            menu_296 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Form báo cáo kho', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_296.id if menu_296 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_176bc4d70e5c4c4cb919046b1475cec6.form', 'model': 'x_176bc4d70e5c4c4cb919046b1475cec6', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name" invisible="1"/>\n            <field name="x_tu_ngay"/>\n            <field name="x_den_ngay"/>\n        </group>\n        <notebook/>\n        <footer>\n            <button name="1" type="action" string="Xác nhận" class="btn-primary"/>\n            <button special="cancel" string="Huỷ" class="btn-secondary"/>\n        </footer>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_176bc4d70e5c4c4cb919046b1475cec6.list', 'model': 'x_176bc4d70e5c4c4cb919046b1475cec6', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_tu_ngay" optional="show"/>\n    <field name="x_den_ngay" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_176bc4d70e5c4c4cb919046b1475cec6.search', 'model': 'x_176bc4d70e5c4c4cb919046b1475cec6', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_tu_ngay"/>\n    <field name="x_den_ngay"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Form báo cáo kho

        groups = []
        field_vals = {'name': 'x_den_ngay', 'field_description': 'Đến ngày', 'ttype': 'date', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': True, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tu_ngay', 'field_description': 'Từ ngày', 'ttype': 'date', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Form báo cáo tổng hợp
        model_vals = {'name': 'Form báo cáo tổng hợp', 'model': 'x_5a4a212c55a341b1a0e0e90a99886031', 'state': 'manual', 'transient': True, 'is_filter_manual': True, 'is_mail_thread': False, 'is_mail_activity': False}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Form báo cáo tổng hợp', 'res_model': 'x_5a4a212c55a341b1a0e0e90a99886031', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': False}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_296_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Popup'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Popup', 'sequence': 10, 'group_ids': [(6, 0, group_296_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_296 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_296:
            menu_296 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Form báo cáo tổng hợp', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_296.id if menu_296 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_5a4a212c55a341b1a0e0e90a99886031.form', 'model': 'x_5a4a212c55a341b1a0e0e90a99886031', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name" invisible="1"/>\n            <field name="x_tu_ngay"/>\n            <field name="x_den_ngay"/>\n        </group>\n        <notebook/>\n        <footer>\n            <button name="1" type="action" string="Xác nhận" class="btn-primary"/>\n            <button special="cancel" string="Huỷ" class="btn-secondary"/>\n        </footer>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_5a4a212c55a341b1a0e0e90a99886031.list', 'model': 'x_5a4a212c55a341b1a0e0e90a99886031', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_tu_ngay" optional="show"/>\n    <field name="x_den_ngay" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_5a4a212c55a341b1a0e0e90a99886031.search', 'model': 'x_5a4a212c55a341b1a0e0e90a99886031', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_tu_ngay"/>\n    <field name="x_den_ngay"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Form báo cáo tổng hợp

        groups = []
        field_vals = {'name': 'x_den_ngay', 'field_description': 'Đến ngày', 'ttype': 'date', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': True, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_tu_ngay', 'field_description': 'Từ ngày', 'ttype': 'date', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        #model Form thanh toán
        model_vals = {'name': 'Form thanh toán', 'model': 'x_657e8bcb071e4f44a8aa9845fbdce258', 'state': 'manual', 'transient': True, 'is_filter_manual': True, 'is_mail_thread': False, 'is_mail_activity': False}
        model_vals['from_app_id'] = custom_module_id.id if custom_module_id else False
        model_id = env['ir.model'].create(model_vals)
        x_name = env['ir.model.fields'].search([('model_id', '=', model_id.id), ('name', '=', 'x_name')], limit=1)
        if x_name:
            x_name.unlink()
        
        #model access right

        group_id = False

        group_id = env['res.groups'].search([('uuid', '=', 'uuid_role_user')], limit=1)

        if not group_id:
            group_vals = {'name': 'Role / User', 'uuid': 'uuid_role_user', 'share': False, 'sequence': 0, 'api_key_duration': 90.0, 'comment': 'Access to the home menu'}
            privilege_id = env['res.groups.privilege'].search([('uuid', '=', 'False')], limit=1)
            if False and not privilege_id:
                privilege_vals = {}
                privilege_id = env['res.groups.privilege'].create(privilege_vals)
            group_vals['privilege_id'] = privilege_id.id if privilege_id else False
            group_id = env['res.groups'].create(group_vals)

        access_vals = {'name': 'Quyền cơ bản', 'perm_read': True, 'perm_write': True, 'perm_create': True, 'perm_unlink': True}
        access_vals['group_id'] = group_id.id if group_id else False
        access_vals['model_id'] = model_id.id
        env['ir.model.access'].create(access_vals)

        
        #model rules

        
        #model menus

        action_group_ids = []

        action_vals = {'name': 'Form thanh toán', 'res_model': 'x_657e8bcb071e4f44a8aa9845fbdce258', 'type': 'ir.actions.act_window', 'usage': False, 'target': 'current', 'cache': True, 'view_mode': 'list,form', 'mobile_view_mode': 'kanban', 'domain': False, 'context': '{}', 'limit': 80, 'filter': False, 'help': False}
        action_vals['group_ids'] = [(6, 0, action_group_ids)]
        action_id = env['ir.actions.act_window'].create(action_vals)

        menu_group_ids = []

        group_296_ids = []

        group_276_ids = []

        group_275_ids = []

        menu_domain = [('name', '=', 'Kế toán'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kế toán', 'sequence': 10, 'group_ids': [(6, 0, group_275_ids)], 'is_custom': True}
        if False:
            menu_domain.append(('parent_id', '=', False.id))
            menu_create_domain['parent_id'] = False.id
        menu_275 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_275:
            menu_275 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Kỹ thuật'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Kỹ thuật', 'sequence': 10, 'group_ids': [(6, 0, group_276_ids)], 'is_custom': True}
        if menu_275:
            menu_domain.append(('parent_id', '=', menu_275.id))
            menu_create_domain['parent_id'] = menu_275.id
        menu_276 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_276:
            menu_276 = env['ir.ui.menu'].create(menu_create_domain)

        menu_domain = [('name', '=', 'Popup'), ('is_custom', '=', True)]
        menu_create_domain = {'name': 'Popup', 'sequence': 10, 'group_ids': [(6, 0, group_296_ids)], 'is_custom': True}
        if menu_276:
            menu_domain.append(('parent_id', '=', menu_276.id))
            menu_create_domain['parent_id'] = menu_276.id
        menu_296 = env['ir.ui.menu'].search(menu_domain, limit=1)
        if not menu_296:
            menu_296 = env['ir.ui.menu'].create(menu_create_domain)

        menu_vals = {'name': 'Form thanh toán', 'sequence': 10, 'is_custom': True}
        menu_vals['action'] = f"ir.actions.act_window,{action_id.id}"
        menu_vals['group_ids'] = [(6, 0, menu_group_ids)]
        menu_vals['parent_id'] = menu_296.id if menu_296 else False
        env['ir.ui.menu'].create(menu_vals)

        
        #model views

        view_group_ids = []

        view_vals = {'name': 'x_657e8bcb071e4f44a8aa9845fbdce258.form', 'model': 'x_657e8bcb071e4f44a8aa9845fbdce258', 'arch_base': '<form>\n    <header/>\n    <sheet>\n        <group>\n            <field name="x_name" invisible="1"/>\n            <field name="x_ngay_thang"/>\n            <field name="x_so_tien"/>\n            <field name="x_loai_thanh_toan"/>\n            <field name="x_chuc_nang"/>\n            <field name="x_hop_dong"/>\n        </group>\n        <notebook/>\n        <footer>\n            <button name="1" type="action" string="Xác nhận" class="btn-primary"/>\n            <button special="cancel" string="Huỷ" class="btn-secondary"/>\n        </footer>\n    </sheet>\n    <chatter/>\n</form>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'form'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_657e8bcb071e4f44a8aa9845fbdce258.list', 'model': 'x_657e8bcb071e4f44a8aa9845fbdce258', 'arch_base': '<list editable="bottom">\n    <field name="x_name" optional="show"/>\n    <field name="x_ngay_thang" optional="show"/>\n    <field name="x_so_tien" optional="show"/>\n    <field name="x_loai_thanh_toan" optional="show"/>\n    <field name="x_chuc_nang" optional="show"/>\n    <field name="x_hop_dong" optional="show"/>\n</list>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'list'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)

        view_group_ids = []

        view_vals = {'name': 'x_657e8bcb071e4f44a8aa9845fbdce258.search', 'model': 'x_657e8bcb071e4f44a8aa9845fbdce258', 'arch_base': '<search>\n    <field name="x_name"/>\n    <field name="x_ngay_thang"/>\n    <field name="x_so_tien"/>\n    <field name="x_loai_thanh_toan"/>\n    <field name="x_chuc_nang"/>\n    <field name="x_hop_dong"/>\n</search>', 'mode': 'primary', 'priority': 16, 'active': True, 'type': 'search'}
        view_vals['group_ids'] = [(6, 0, view_group_ids)]
        view_vals['model_id'] = model_id.id
        views_payloads.append(view_vals)


        #prepare fields for model Form thanh toán

        groups = []
        field_vals = {'name': 'x_chuc_nang', 'field_description': 'Chức năng', 'ttype': 'selection', 'help': False, 'sequence': 5, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Xoá cũ tạo mới', 'name': 'Xoá cũ tạo mới'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Thêm tiền', 'name': 'Thêm tiền'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_hop_dong', 'field_description': 'Hợp đồng', 'ttype': 'many2one', 'help': False, 'sequence': 6, 'relation': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': 'set null', 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_loai_thanh_toan', 'field_description': 'Loại thanh toán', 'ttype': 'selection', 'help': False, 'sequence': 4, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['selection_vals'].append({'sequence': 0, 'value': 'Tiền mặt', 'name': 'Tiền mặt'})

        field_vals['selection_vals'].append({'sequence': 1, 'value': 'Ngân hàng', 'name': 'Ngân hàng'})

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_name', 'field_description': 'Name', 'ttype': 'char', 'help': False, 'sequence': 1, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': True, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_ngay_thang', 'field_description': 'Ngày tháng', 'ttype': 'datetime', 'help': False, 'sequence': 2, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

        groups = []
        field_vals = {'name': 'x_so_tien', 'field_description': 'Số tiền', 'ttype': 'float', 'help': False, 'sequence': 3, 'relation': False, 'relation_field': False, 'relation_table': False, 'column1': False, 'column2': False, 'on_delete': False, 'domain': '[]', 'related': False, 'depends': False, 'compute': False, 'required': False, 'readonly': False, 'invisible': False, 'store': True, 'index': False, 'copied': True, 'tracking': 0, 'approval_field': False}
        field_vals['model_id'] = model_id.id
        field_vals['selection_vals'] = []

        field_vals['groups_vals'] = groups

        fields_payloads.append(field_vals)

    create_models()

    
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
            update_fields.append({
                'id': field_id.id,
                'related': related,
                'depends': depends,
                'compute': compute,
            })
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
        field_id.write({
            'related': field['related'],
            'depends': field['depends'],
            'compute': field['compute'],
        })

    
    #models automation

    model_id = env['ir.model'].search([('model', '=', 'x_b5d5cecc141e40a3925a41923922bcc2')])

    model_id = env['ir.model'].search([('model', '=', 'x_f19155e4689c401ea07a09b90a63f794')])

    model_id = env['ir.model'].search([('model', '=', 'x_8d898fdcdadf451f844fa3ba69f9c226')])

    model_id = env['ir.model'].search([('model', '=', 'x_5579eb7c8c8f454cb54cd8e85234d153')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Hợp đồng', 'implementation': 'standard', 'code': 'x_5579eb7c8c8f454cb54cd8e85234d153', 'active': True, 'prefix': 'HD-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Hợp đồng', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_5579eb7c8c8f454cb54cd8e85234d153')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_5579eb7c8c8f454cb54cd8e85234d153'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\nrecord.write({"x_ngay_thang": datetime.datetime.today()})', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kế toán", [("x_loai_chung_tu", "=", REF_ID)])\nDELETE("Mua bán hàng hoá", [("x_so_hd", "=", record.id)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_a6da8efa11194f1bae3b7522c10e954b')])

    model_id = env['ir.model'].search([('model', '=', 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Mua bán hàng hoá', 'implementation': 'standard', 'code': 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8', 'active': True, 'prefix': 'MBHH-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Mua bán hàng hoá', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'Tạo sổ cái kho', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Tính giá vốn', 'sequence': 5, 'state': 'code', 'code': 'def clean_ledger(ledger):\n    positive = [i for i in ledger if i > 0]\n    negative = sum(1 for i in ledger if i < 0)\n    return positive[negative:]\n\ndef get_rate(ledger, amount):\n    if not amount:\n            return 0\n    left = ledger[:amount]\n    right = ledger[amount:]\n    return sum(left) / amount\n\ndomain = [("x_kho_hang", "=", record.x_kho_hang.id), ("x_hang_hoa", "=", record.x_hang_hoa.id)]\n\nif record.x_muc_dich == "Xuất":\n    r = EXPAND_ARRAY("Sổ cái kho", "value:x_gia_von, multi:x_so_luong, before:x_ngay_thang", domain)\n    a = clean_ledger(r)\n\n    rate = get_rate(a, int(record.x_so_luong))\n    if rate != record.x_gia_von:\n        record.write({"x_gia_von": rate})\nelif record.x_muc_dich == "Nhập":\n    if not record.x_don_gia:\n        record.write({\n            "x_don_gia": record.x_hang_hoa.x_gia_ban,\n            "x_gia_von": record.x_hang_hoa.x_gia_ban\n        })\n    else:\n        record.write({"x_gia_von": record.x_don_gia})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Tạo sổ cái', 'sequence': 6, 'state': 'code', 'code': 'x_so_luong = record.x_so_luong\n\nif record.x_muc_dich == "Xuất":\n    x_so_luong = -record.x_so_luong\n\nCREATE_OR_WRITE("Sổ cái kho", "x_loai_chung_tu, x_kho_hang", {\n    "x_loai_chung_tu": REF_ID,\n    "x_kho_hang": record.x_kho_hang.id,\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_so_luong": x_so_luong,\n    "x_gia_von": record.x_gia_von,\n    "x_muc_dich": record.x_muc_dich,\n    "x_hang_hoa": record.x_hang_hoa.id,\n    "x_cong_ty": record.x_cong_ty.id\n}, "x_kho_hang")\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'tạo sổ cái kế toán', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'sck_name = "Sổ cái kế toán"\nvoucher_type = REF(model.x_so_hd._name, record.x_so_hd.id)\n\nco_ban = any([r.x_muc_dich == "Xuất" for r in record.x_so_hd.x_items])\nco_mua = any([r.x_muc_dich == "Nhập" for r in record.x_so_hd.x_items])\n\ntong_dinh_gia_ban = sum([r.x_so_luong * r.x_gia_von for r in record.x_so_hd.x_items if r.x_muc_dich == "Xuất"])\ntong_gia_tri_ban = sum([r.x_so_luong * r.x_don_gia for r in record.x_so_hd.x_items if r.x_muc_dich == "Xuất"])\ntong_dinh_gia_mua = sum([r.x_so_luong * r.x_gia_von for r in record.x_so_hd.x_items if r.x_muc_dich == "Nhập"])\ntong_gia_tri_mua = sum([r.x_so_luong * r.x_don_gia for r in record.x_so_hd.x_items if r.x_muc_dich == "Nhập"])\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_ghi_chu": "Xuất",\n    "x_account_type": "Stock",\n    "x_tai_khoan": record.x_so_hd.x_cong_ty.x_tai_khoan_kho.id,\n    "x_tai_khoan_doi_ung": record.x_so_hd.x_cong_ty.x_tai_khoan_chi_phi.x_name,\n\n    "x_ngay_thang": record.x_so_hd.x_ngay_thang,\n    "x_credit": tong_dinh_gia_ban,\n    "x_doi_tac": record.x_so_hd.x_doi_tac.id,\n    "x_cong_ty": record.x_so_hd.x_cong_ty.id\n}, "x_account_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_account_type": "Cost of Goods Sold",\n    "x_ghi_chu": "Cost of Goods Sold",\n    "x_tai_khoan": record.x_so_hd.x_cong_ty.x_tai_khoan_chi_phi.id,\n    "x_tai_khoan_doi_ung": record.x_so_hd.x_cong_ty.x_tai_khoan_kho.x_name,\n\n    "x_ngay_thang": record.x_so_hd.x_ngay_thang,\n    "x_debit": tong_dinh_gia_ban,\n    "x_doi_tac": record.x_so_hd.x_doi_tac.id,\n    "x_cong_ty": record.x_so_hd.x_cong_ty.id\n}, "x_account_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_account_type": "Receivable",\n    "x_ghi_chu": "Receivable",\n    "x_tai_khoan": record.x_so_hd.x_cong_ty.x_tai_khoan_phai_thu.id,\n    "x_tai_khoan_doi_ung": record.x_so_hd.x_cong_ty.x_tai_khoan_doanh_thu.x_name,\n\n    "x_ngay_thang": record.x_so_hd.x_ngay_thang,\n    "x_debit": tong_gia_tri_ban,\n    "x_doi_tac": record.x_so_hd.x_doi_tac.id,\n    "x_cong_ty": record.x_so_hd.x_cong_ty.id\n}, "x_account_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_root_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_root_type": "Income",\n    "x_ghi_chu": "Income",\n    "x_tai_khoan": record.x_so_hd.x_cong_ty.x_tai_khoan_doanh_thu.id,\n    "x_tai_khoan_doi_ung": record.x_so_hd.x_cong_ty.x_tai_khoan_phai_thu.x_name,\n\n    "x_ngay_thang": record.x_so_hd.x_ngay_thang,\n    "x_credit": tong_gia_tri_ban,\n    "x_doi_tac": record.x_so_hd.x_doi_tac.id,\n    "x_cong_ty": record.x_so_hd.x_cong_ty.id\n}, "x_root_type", co_ban)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_ghi_chu": "Nhập",\n    "x_account_type": "Stock",\n    "x_tai_khoan": record.x_so_hd.x_cong_ty.x_tai_khoan_kho.id,\n    "x_tai_khoan_doi_ung": record.x_so_hd.x_cong_ty.x_tai_khoan_phai_tra.x_name,\n\n    "x_ngay_thang": record.x_so_hd.x_ngay_thang,\n    "x_debit": tong_dinh_gia_mua,\n    "x_doi_tac": record.x_so_hd.x_doi_tac.id,\n    "x_cong_ty": record.x_so_hd.x_cong_ty.id\n}, "x_account_type", co_mua)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_account_type": "Payable",\n    "x_ghi_chu": "Payable",\n    "x_tai_khoan": record.x_so_hd.x_cong_ty.x_tai_khoan_phai_tra.id,\n    "x_tai_khoan_doi_ung": record.x_so_hd.x_cong_ty.x_tai_khoan_kho.x_name,\n\n    "x_ngay_thang": record.x_so_hd.x_ngay_thang,\n    "x_credit": tong_dinh_gia_mua,\n    "x_doi_tac": record.x_so_hd.x_doi_tac.id,\n    "x_cong_ty": record.x_so_hd.x_cong_ty.id\n}, "x_account_type", co_mua)\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'on delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kho", [("x_loai_chung_tu", "=", REF_ID)])\nDELETE("Nhật ký thanh toán", [("x_mua_ban_hang_hoa", "=", record.id)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Thanh toán', 'sequence': 5, 'state': 'code', 'code': 'action2 = ACT_WINDOW("Form thanh toán")\n\naction2["context"] = {\n    "default_x_hop_dong": record.x_so_hd.id,\n}\naction = action2', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if True:
        binding_model_id = env['ir.model'].search([('model', '=', 'x_bea12ff7f1fe4f6fadf098f0f84ab7d8')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_4b01b3eb8ec04fff8d7a74437491f315')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Nghiệp vụ khác', 'implementation': 'standard', 'code': 'x_4b01b3eb8ec04fff8d7a74437491f315', 'active': True, 'prefix': 'NVK-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Nghiệp vụ khác', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_4b01b3eb8ec04fff8d7a74437491f315')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_4b01b3eb8ec04fff8d7a74437491f315'), ('name', '=', 'display_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\nrecord.write({"x_ngay_thang": datetime.datetime.now()})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_4b01b3eb8ec04fff8d7a74437491f315'), ('name', '=', 'x_cong_ty')])
    on_change_field_ids.append(field_id.id)

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_4b01b3eb8ec04fff8d7a74437491f315'), ('name', '=', 'x_ghi_chu')])
    on_change_field_ids.append(field_id.id)

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_4b01b3eb8ec04fff8d7a74437491f315'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_4b01b3eb8ec04fff8d7a74437491f315'), ('name', '=', 'x_ngay_thang')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'set items ngày tháng', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'record.x_items.write({\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_cong_ty": record.x_cong_ty.id,\n    "x_ghi_chu": record.x_ghi_chu\n})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'set items ngày tháng after edit', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'record.x_items.write({\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_cong_ty": record.x_cong_ty.id,\n    "x_ghi_chu": record.x_ghi_chu\n})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kế toán", [("x_loai_chung_tu", "=", REF_ID)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_0cb7fa70192b4a6eab9403509aa45ca0')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Nhật ký thanh toán', 'implementation': 'standard', 'code': 'x_0cb7fa70192b4a6eab9403509aa45ca0', 'active': True, 'prefix': 'NKTT-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Nhật ký thanh toán', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_0cb7fa70192b4a6eab9403509aa45ca0')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'Tạo sổ cái kế toán', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'sck_name = "Sổ cái kế toán"\nvoucher_type = REF_ID\n\nx_tai_khoan_doi_ung = record.x_cong_ty.x_tai_khoan_tien_mat.x_name\nx_tai_khoan_doi_ung_tt = record.x_cong_ty.x_tai_khoan_phai_thu.x_name\nx_debit_tt = record.x_thanh_toan\nx_credit_tt = 0\n\nif record.x_loai_thanh_toan == "Ngân hàng":\n    x_tai_khoan_doi_ung = record.x_cong_ty.x_tai_khoan_ngan_hang.x_name\nif record.x_mua_ban_hang_hoa.x_muc_dich == "Nhập":\n    x_tai_khoan_doi_ung_tt = record.x_cong_ty.x_tai_khoan_phai_tra.x_name\n    x_debit_tt = 0\n    x_credit_tt = record.x_thanh_toan\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_account_type": "Receivable",\n    "x_ghi_chu": "Receivable",\n    "x_tai_khoan": record.x_mua_ban_hang_hoa.x_cong_ty.x_tai_khoan_phai_thu.id,\n    "x_tai_khoan_doi_ung": x_tai_khoan_doi_ung,\n\n    "x_ngay_thang": record.x_mua_ban_hang_hoa.x_ngay_thang,\n    "x_credit": record.x_thanh_toan,\n    "x_dai_ly": record.x_mua_ban_hang_hoa.x_dai_ly.id,\n    "x_cong_ty": record.x_mua_ban_hang_hoa.x_cong_ty.id\n}, "x_account_type", record.x_mua_ban_hang_hoa.x_muc_dich == "Xuất")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_account_type": "Payable",\n    "x_ghi_chu": "Payable",\n    "x_tai_khoan": record.x_mua_ban_hang_hoa.x_cong_ty.x_tai_khoan_phai_tra.id,\n    "x_tai_khoan_doi_ung": x_tai_khoan_doi_ung,\n\n    "x_ngay_thang": record.x_mua_ban_hang_hoa.x_ngay_thang,\n    "x_debit": record.x_thanh_toan,\n    "x_dai_ly": record.x_mua_ban_hang_hoa.x_dai_ly.id,\n    "x_cong_ty": record.x_mua_ban_hang_hoa.x_cong_ty.id\n}, "x_account_type", record.x_mua_ban_hang_hoa.x_muc_dich == "Nhập")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_account_type": "Cash",\n    "x_ghi_chu": "Cash",\n    "x_tai_khoan": record.x_mua_ban_hang_hoa.x_cong_ty.x_tai_khoan_tien_mat.id,\n    "x_tai_khoan_doi_ung": x_tai_khoan_doi_ung_tt,\n\n    "x_ngay_thang": record.x_mua_ban_hang_hoa.x_ngay_thang,\n    "x_debit": x_debit_tt,\n    "x_credit": x_credit_tt,\n    "x_dai_ly": record.x_mua_ban_hang_hoa.x_dai_ly.id,\n    "x_cong_ty": record.x_mua_ban_hang_hoa.x_cong_ty.id\n}, "x_account_type", record.x_loai_thanh_toan == "Tiền mặt")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": voucher_type,\n    "x_account_type": "Bank",\n    "x_ghi_chu": "Bank",\n    "x_tai_khoan": record.x_mua_ban_hang_hoa.x_cong_ty.x_tai_khoan_ngan_hang.id,\n    "x_tai_khoan_doi_ung": x_tai_khoan_doi_ung_tt,\n\n    "x_ngay_thang": record.x_mua_ban_hang_hoa.x_ngay_thang,\n    "x_debit": x_debit_tt,\n    "x_credit": x_credit_tt,\n    "x_dai_ly": record.x_mua_ban_hang_hoa.x_dai_ly.id,\n    "x_cong_ty": record.x_mua_ban_hang_hoa.x_cong_ty.id\n}, "x_account_type", record.x_loai_thanh_toan == "Ngân hàng")\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kho", [("x_loai_chung_tu", "=", REF_ID)])\nDELETE("Sổ cái kế toán", [("x_loai_chung_tu", "=", REF_ID)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_2d75d5f44f924a9282735b054b0007a1')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Phiếu kho', 'implementation': 'standard', 'code': 'x_2d75d5f44f924a9282735b054b0007a1', 'active': True, 'prefix': 'PHK-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Phiếu kho', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_2d75d5f44f924a9282735b054b0007a1')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_2d75d5f44f924a9282735b054b0007a1'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()\nrecord.write({"x_ngay_thang": datetime.datetime.today()})', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kế toán", [("x_loai_chung_tu", "=", REF_ID)])\nDELETE("Xuất nhập kho", [("x_phieu_kho", "=", record.id)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_c78095f0ddb645eca0cd38dee357725c')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Sổ cái kho', 'implementation': 'standard', 'code': 'x_c78095f0ddb645eca0cd38dee357725c', 'active': True, 'prefix': 'SCK-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Sổ cái kho', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_c78095f0ddb645eca0cd38dee357725c')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Tạo báo cáo', 'sequence': 5, 'state': 'code', 'code': 'action = ACT_WINDOW("Form báo cáo kho")', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if True:
        binding_model_id = env['ir.model'].search([('model', '=', 'x_c78095f0ddb645eca0cd38dee357725c')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_e4a49df8fa1c4db9a0d729719332b9eb')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'thiết lập bút toán điều chỉnh chứng từ', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'ref_id = REF(record.x_nghiep_vu_khac._name, record.x_nghiep_vu_khac.id)\nif record.x_nghiep_vu_khac:\n    record.write({"x_loai_chung_tu": ref_id})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Sổ cái kế toán', 'implementation': 'standard', 'code': 'x_e4a49df8fa1c4db9a0d729719332b9eb', 'active': True, 'prefix': 'SKCT-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Sổ cái kế toán', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_e4a49df8fa1c4db9a0d729719332b9eb')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_e4a49df8fa1c4db9a0d729719332b9eb'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Tạo báo cáo', 'sequence': 5, 'state': 'code', 'code': 'action = ACT_WINDOW("Form báo cáo tổng hợp")', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if True:
        binding_model_id = env['ir.model'].search([('model', '=', 'x_e4a49df8fa1c4db9a0d729719332b9eb')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_6fc605916fea47c3bbd6da0a25660665')])

    model_id = env['ir.model'].search([('model', '=', 'x_1252b666e8a04a17930b0c4166d12b43')])

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'ref', 'trigger': 'on_create', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    sequence_id = env['ir.sequence'].create({'name': 'Xuất nhập kho', 'implementation': 'standard', 'code': 'x_1252b666e8a04a17930b0c4166d12b43', 'active': True, 'prefix': 'XNK-', 'suffix': False, 'padding': 4, 'number_increment': 1, 'use_date_range': False})

    action_vals = {'name': 'Update Xuất nhập kho', 'sequence': 5, 'state': 'object_write', 'code': False, 'evaluation_type': 'sequence', 'update_path': 'x_name', 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'x_name'), ('model', '=', 'x_1252b666e8a04a17930b0c4166d12b43')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_1252b666e8a04a17930b0c4166d12b43'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DISPLAY_SEQUENCE()', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'Tạo sổ cái', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Tính giá vốn', 'sequence': 5, 'state': 'code', 'code': 'def clean_ledger(ledger):\n    positive = [i for i in ledger if i > 0]\n    negative = sum(1 for i in ledger if i < 0)\n    return positive[negative:]\n\ndef get_rate(ledger, amount):\n    if not amount:\n            return 0\n    left = ledger[:amount]\n    right = ledger[amount:]\n    return sum(left) / amount\n\ndomain = [("x_kho_hang", "=", record.x_kho_nguon.id), ("x_hang_hoa", "=", record.x_hang_hoa.id)]\n\nif record.x_muc_dich == "Xuất":\n    r = EXPAND_ARRAY("Sổ cái kho", "value:x_gia_von, multi:x_so_luong, before:x_ngay_thang", domain)\n    a = clean_ledger(r)\n\n    rate = get_rate(a, int(record.x_so_luong))\n    if rate != record.x_gia_tri:\n        record.write({"x_gia_tri": rate})\nelif record.x_muc_dich == "Nhập" and not record.x_gia_tri:\n    record.write({"x_gia_tri": record.x_hang_hoa.x_gia_ban})\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Tạo sổ cái kho', 'sequence': 6, 'state': 'code', 'code': 'sck_name = "Sổ cái kho"\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_kho_hang, x_ghi_chu", {\n    "x_loai_chung_tu": REF_ID,\n    "x_kho_hang": record.x_kho_dich.id,\n    "x_ghi_chu": "Kho đích",\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_so_luong": record.x_so_luong,\n    "x_gia_von": record.x_gia_tri,\n    "x_muc_dich": record.x_muc_dich,\n    "x_hang_hoa": record.x_hang_hoa.id,\n    "x_cong_ty": record.x_cong_ty.id\n}, "x_kho_hang")\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_kho_hang, x_ghi_chu", {\n    "x_loai_chung_tu": REF_ID,\n    "x_kho_hang": record.x_kho_nguon.id,\n    "x_ghi_chu": "Kho nguồn",\n    "x_ngay_thang": record.x_ngay_thang,\n    "x_so_luong": -record.x_so_luong,\n    "x_gia_von": record.x_gia_tri,\n    "x_muc_dich": record.x_muc_dich,\n    "x_hang_hoa": record.x_hang_hoa.id,\n    "x_cong_ty": record.x_cong_ty.id\n}, "x_kho_hang", record.x_muc_dich == "Xuất")\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'Tạo sổ cái kế toán', 'trigger': 'on_create_or_write', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'sck_name = "Sổ cái kế toán"\n\ntong_dinh_gia = sum([r.x_so_luong * r.x_gia_tri for r in record.x_phieu_kho.x_items])\nreference_id = REF(record.x_phieu_kho._name, record.x_phieu_kho.id)\nnhap_hang = record.x_muc_dich == "Nhập"\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": reference_id,\n    "x_tai_khoan": record.x_phieu_kho.x_cong_ty.x_tai_khoan_kho.id,\n    "x_account_type": "Stock",\n    "x_ghi_chu": "Stock",\n    "x_ngay_thang": record.x_phieu_kho.x_ngay_thang,\n    "x_debit": tong_dinh_gia,\n    "x_tai_khoan_doi_ung": record.x_phieu_kho.x_cong_ty.x_tai_khoan_dieu_chinh.x_name,\n    "x_cong_ty": record.x_phieu_kho.x_cong_ty.id\n}, "x_account_type", nhap_hang)\n\nCREATE_OR_WRITE(sck_name, "x_loai_chung_tu, x_account_type, x_ghi_chu", {\n    "x_loai_chung_tu": reference_id,\n    "x_tai_khoan": record.x_phieu_kho.x_cong_ty.x_tai_khoan_dieu_chinh.id,\n    "x_account_type": "Stock Adjustment",\n    "x_ghi_chu": "Stock Adjustment",\n    "x_ngay_thang": record.x_phieu_kho.x_ngay_thang,\n    "x_credit": tong_dinh_gia,\n    "x_tai_khoan_doi_ung": record.x_phieu_kho.x_cong_ty.x_tai_khoan_kho.x_name,\n    "x_cong_ty": record.x_phieu_kho.x_cong_ty.id\n}, "x_account_type", nhap_hang)\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    trigger_field_ids = []
    on_change_field_ids = []

    auto_vals = {'name': 'on delete', 'trigger': 'on_unlink', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'DELETE("Sổ cái kho", [("x_loai_chung_tu", "=", REF_ID)])\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_00c5b25ba4f54ad085e01b57b20eb8a9')])

    model_id = env['ir.model'].search([('model', '=', 'x_176bc4d70e5c4c4cb919046b1475cec6')])

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'ok', 'sequence': 5, 'state': 'code', 'code': 'sck_id = UNIQUE_MODEL("Sổ cái kho")\nx_nhat_ky_mua_ban = UNIQUE_MODEL("Mua bán hàng hoá")\n\ntdk = sck_id.search([("x_ngay_thang", "<", record.x_tu_ngay)])\nttk = sck_id.search([\n    ("x_ngay_thang", ">=", record.x_tu_ngay), ("x_ngay_thang", "<=", record.x_den_ngay), ("x_loai_chung_tu", "not like", x_nhat_ky_mua_ban._name + ",")\n])\nttk2 = sck_id.search([\n    ("x_ngay_thang", ">=", record.x_tu_ngay), \n    ("x_ngay_thang", "<=", record.x_den_ngay), \n    ("x_loai_chung_tu", "like", x_nhat_ky_mua_ban._name + ","),\n    ("x_so_luong", ">", 0)\n])\nxbtk = sck_id.search([\n    ("x_ngay_thang", ">=", record.x_tu_ngay), \n    ("x_ngay_thang", "<=", record.x_den_ngay), \n    ("x_loai_chung_tu", "like", x_nhat_ky_mua_ban._name + ","),\n    ("x_so_luong", "<", 0)\n])\nleft = sck_id.search([("x_ngay_thang", ">", record.x_den_ngay)])\nleft.write({"x_loai_ky": ""})\ntdk.write({"x_loai_ky": "Tồn đầu kỳ"})\nttk.write({"x_loai_ky": "Nhập trong kỳ"})\nttk2.write({"x_loai_ky": "Nhập trong kỳ"})\nxbtk.write({"x_loai_ky": "Xuất bán trong kỳ"})\n\nact = ACT_WINDOW("Sổ cái kho")\nact["name"] = f"Báo cáo kho ngày {record.x_tu_ngay} đến ngày {record.x_den_ngay}"\nact["target"] = "current"\nact["view_mode"] = "pivot"\nact["views"] = [(False, "pivot")]\naction = act', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_5a4a212c55a341b1a0e0e90a99886031')])

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'ok', 'sequence': 5, 'state': 'code', 'code': 'act = ACT_WINDOW("Sổ cái kế toán")\nact["name"] = f"Báo cáo tổng hợp ngày {record.x_tu_ngay} đến ngày {record.x_den_ngay}"\nact["target"] = "current"\nact["view_mode"] = "pivot"\nact["views"] = [(False, "pivot")]\nact["domain"] = [("x_ngay_thang", ">=", record.x_tu_ngay), ("x_ngay_thang", "<=", record.x_den_ngay)]\naction = act\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    model_id = env['ir.model'].search([('model', '=', 'x_657e8bcb071e4f44a8aa9845fbdce258')])

    trigger_field_ids = []
    on_change_field_ids = []

    field_id = env['ir.model.fields'].search([('model_id', '=', 'x_657e8bcb071e4f44a8aa9845fbdce258'), ('name', '=', 'x_name')])
    on_change_field_ids.append(field_id.id)

    auto_vals = {'name': 'default', 'trigger': 'on_change', 'filter_pre_domain': False, 'previous_domain': False, 'filter_domain': False, 'description': False}
    auto_vals['model_id'] = model_id.id
    auto_vals['trigger_field_ids'] = [(6, 0, trigger_field_ids)]
    auto_vals['on_change_field_ids'] = [(6, 0, on_change_field_ids)]
    auto_id = env['base.automation'].create(auto_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'Execute Code', 'sequence': 5, 'state': 'code', 'code': 'record.write({\n    "x_ngay_thang": datetime.datetime.now(),\n    "x_loai_thanh_toan": "Tiền mặt",\n    "x_chuc_nang": "Xoá cũ tạo mới"\n})', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['base_automation_id'] = auto_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    action_group_ids = []

    sequence_id = False

    action_vals = {'name': 'ok', 'sequence': 5, 'state': 'code', 'code': 'if record.x_chuc_nang == "Thêm tiền":\n    raise UserError("Chưa triển khai chức năng này!")\n\nrecord.x_hop_dong.x_items.x_nhat_ky_thanh_toan.unlink()\n\ntotal = record.x_so_tien\n\nfor nk in record.x_hop_dong.x_items:\n    if total >= nk.x_thanh_tien:\n        CREATE("Nhật ký thanh toán", {\n            "x_ngay_thang": record.x_ngay_thang,\n            "x_loai_thanh_toan": record.x_loai_thanh_toan,\n            "x_thanh_toan": nk.x_thanh_tien,\n            "x_mua_ban_hang_hoa": nk.id\n        })\n        total -= nk.x_thanh_tien\n    else:\n        CREATE("Nhật ký thanh toán", {\n            "x_ngay_thang": record.x_ngay_thang,\n            "x_loai_thanh_toan": record.x_loai_thanh_toan,\n            "x_thanh_toan": total,\n            "x_mua_ban_hang_hoa": nk.id\n        })\n        break\n', 'evaluation_type': 'value', 'update_path': False, 'value': False, 'binding_type': 'action'}
    if sequence_id:
        # field_id = env['ir.model.fields'].search([('name', '=', 'False'), ('model', '=', 'False')], limit=1)
        # action_vals['update_field_id'] = field_id.id if field_id else False
        action_vals['sequence_id'] = sequence_id.id if sequence_id else False
    if False:
        binding_model_id = env['ir.model'].search([('model', '=', 'False')], limit=1)
        action_vals['binding_model_id'] = binding_model_id.id
    action_vals['model_id'] = model_id.id
    action_vals['group_ids'] = [(6, 0, action_group_ids)]
    env['ir.actions.server'].create(action_vals)

    
    for view in views_payloads:
        view_id = env['ir.ui.view'].create(view)
        view_id.remove_transient_footer()
        view_id.update_transient_ok_button()


def uninstall_hook(env):
    rec = env['nosheet.custom.app'].search([('uuid', '=', 'uuid_76d79d5175fb48398ee0ba4ee6e11660')], limit=1)

    if rec:
        rec.unlink()
