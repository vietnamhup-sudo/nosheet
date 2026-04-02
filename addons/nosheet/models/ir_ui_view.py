from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os

class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    is_editable = fields.Boolean(string="Is Editable", default=True)

    def update_view(self):
        if self.type == 'list':
            return self.update_list_view()
        elif self.type == 'form':
            return self.update_form_view()
        elif self.type == 'search':
            return self.update_search_view()

    def get_custom_fields(self):
        one2many = lambda s: s.ttype == "one2many"
        field_ids = self.model_id.field_id.filtered(lambda f: f.state == 'manual').sorted(key=lambda self: self.sequence)
        return field_ids.filtered(lambda s: not one2many(s)), field_ids.filtered(one2many)

    def update_list_view(self):
        normal_field_ids, one2many_fields = self.get_custom_fields()

        atts = {}
        if self.is_editable:
            atts["editable"] = "bottom"

        root = ET.Element("list", atts)

        for field in normal_field_ids:
            ET.SubElement(root, "field", {
                "name": field.name,
                "optional": "show"
            })

        for field in one2many_fields:
            ET.SubElement(root, "field", {
                "name": field.name,
                "widget": "many2many_tags",
                "optional": "show"
            })
        
        ET.indent(root, space="    ")
        new_xml = ET.tostring(root, encoding="unicode")
        self.arch_base = new_xml

    def update_form_view(self):
        normal_field_ids, one2many_fields = self.get_custom_fields()
        field_ids = normal_field_ids.filtered(lambda f: not f.approval_field)
        approval_fields = normal_field_ids.filtered(lambda f: f.approval_field)

        form = ET.Element("form")

        # header
        header = ET.SubElement(form, "header")
        for field in approval_fields:
            ET.SubElement(header, "field", {
                "name": field.name,
                "widget": "statusbar",
                "options": "{'clickable': 1}"
            })

        # sheet
        sheet = ET.SubElement(form, "sheet")

        # group
        group = ET.SubElement(sheet, "group")
        for field in field_ids:
            attrs = {
                "name": field.name,
            }
            if field.invisible:
                attrs["invisible"] = "1"
            ET.SubElement(group, "field", attrs)

        # notebook
        notebook = ET.SubElement(sheet, "notebook")
        for field in one2many_fields:
            page = ET.SubElement(notebook, "page", {
                "string": field.field_description,
                "name": field.name
            })
            ET.SubElement(page, "field", {
                "name": field.name
            })

        # footer
        if self.model_id.transient:
            footer = ET.SubElement(sheet, "footer")
            ok_action = self.env["ir.actions.server"].search([('name', '=', 'ok'), ("model_id", "=", self.model_id.id)], limit=1)
            if ok_action:
                ET.SubElement(footer, "button", {
                    "name": f"{ok_action.id}",
                    "type": "action",
                    "string": "Xác nhận",
                    "class": "btn-primary"
                })

            ET.SubElement(footer, "button", {
                "special": "cancel",
                "string": "Huỷ",
                "class": "btn-secondary"
            })

        # chatter
        ET.SubElement(form, "chatter")

        ET.indent(form, space="    ")
        new_xml = ET.tostring(form, encoding="unicode")


        self.arch_base = new_xml

    def update_search_view(self):
        normal_field_ids, one2many_fields = self.get_custom_fields()

        root = ET.Element("search")

        for field in normal_field_ids:
            ET.SubElement(root, "field", {
                "name": field.name
            })
        
        ET.indent(root, space="    ")
        new_xml = ET.tostring(root, encoding="unicode")
        self.arch_base = new_xml

    def remove_transient_footer(self):
        if not self.model_id.transient or self.type != 'form':
            return

        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        root = ET.fromstring(self.arch_base, parser=parser)

        for sheet in root.iter("sheet"):
            for footer in sheet.iter("footer"):
                sheet.remove(footer)

        ET.indent(root, space="    ")
        new_xml = ET.tostring(root, encoding="unicode")
        self.arch_base = new_xml

    def update_transient_ok_button(self):
        if not self.model_id.transient or self.type != 'form':
            return

        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        root = ET.fromstring(self.arch_base, parser=parser)
        for sheet in root.iter("sheet"):
            footer = ET.SubElement(sheet, "footer")
            ok_action = self.env["ir.actions.server"].search([('name', '=', 'ok'), ("model_id", "=", self.model_id.id)], limit=1)
            if ok_action:
                ET.SubElement(footer, "button", {
                    "name": f"{ok_action.id}",
                    "type": "action",
                    "string": "Xác nhận",
                    "class": "btn-primary"
                })

            ET.SubElement(footer, "button", {
                "special": "cancel",
                "string": "Huỷ",
                "class": "btn-secondary"
            })

        ET.indent(root, space="    ")
        new_xml = ET.tostring(root, encoding="unicode")
        self.arch_base = new_xml
