from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid
from odoo.fields import Command, Domain
import xml.etree.ElementTree as ET
import os
import unicodedata
import re

def dash_text(text):
    text = unicodedata.normalize('NFD', text)
    text = "".join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.replace('đ', 'd').replace('Đ', 'D')
    text = "_".join(text.split(" "))
    return text.lower()

class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    field_description = fields.Char(string='Field Label', default='', required=True, translate=True, tracking=True)

    invisible = fields.Boolean("Invisible", default=False)
    approval_field = fields.Boolean("Approval Field", default=False)
    sequence = fields.Integer("Sequence", default=1)
    selected_model_id = fields.Many2one(
        'ir.model', 
        string='Model',
    )
    selected_field_id = fields.Many2one(
        'ir.model.fields',
        string='Relation Field',
        domain="[('state', '=', 'manual'), ('model_id', '=', selected_model_id)]"
    )

    from_app_id = fields.Many2one(
        'nosheet.custom.app',
        related='model_id.from_app_id',
        string='From App',
    )

    @api.onchange('field_description')
    def _onchange_field_description(self):
        for record in self:
            name = "x_" + dash_text(record.field_description)
            if record.name != name:
                record.name = name

    @api.onchange('selected_model_id')
    def _onchange_selected_model_id(self):
        for record in self:
            if record.selected_model_id:
                record.relation = record.selected_model_id.model
            else:
                record.relation = ""
    @api.onchange('selected_field_id')
    def _onchange_selected_field_id(self):
        for record in self:
            if record.selected_field_id:
                record.relation_field = record.selected_field_id.name
            else:
                record.relation_field = ""

    def has_field(self, root, field_name):
        for field in root.iter("field"):
            if field.attrib.get("name") == field_name:
                return True
        return False

    def update_view(self):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        t_field = self.env['ir.model.fields'].search([
            ('model', '=', self.model_id.model),
            ('state', '=', 'manual'),
            ('sequence', '<=', self.sequence - 1)
            ], 
        order='sequence desc',
        limit=1)
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)
            if self.has_field(root, self.name):
                continue
            for parent in root.iter():
                children = list(parent)

                for i, child in enumerate(children):
                    if child.tag == "field" and child.attrib.get("name") == t_field.name:

                        new_field = ET.Element("field", {
                            "name": self.name
                        })
                        if view.type == "list":
                            if self.ttype in ["many2many", "one2many"]:
                                new_field.set("widget", "many2many_tags")
                            new_field.set("optional", "show")

                        parent.insert(i + 1, new_field)

                        break
            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")
            view.arch_base = new_xml

    def comment_field_view(self, new_name, old_name):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)

            if self.has_field(root, new_name):
                continue
            for parent in root.iter():
                children = list(parent)

                for i, child in enumerate(children):
                    if child.tag == "field" and child.attrib.get("name") == old_name:

                        child.set("name", new_name)
                        full_tag = ET.tostring(child, encoding="unicode").strip()
                        comment = ET.Comment(f"WHATSUP,{full_tag}")

                        parent.insert(i, comment)
                        parent.remove(child)
            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")

            view.arch_base = new_xml

    def uncomment_field_view(self):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)
            for parent in root.iter():
                children = list(parent)
                for i, child in enumerate(children):
                    if child.tag is ET.Comment:
                        text = (child.text or "").strip()
                        if not text.startswith("WHATSUP,"):
                            continue
                        text = text.replace("WHATSUP,", "", 1).strip()
                        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
                        field = ET.fromstring(text, parser=parser)
                        if field.tag == "field" and field.attrib.get("name") == self.name:
                            parent.insert(i, field)
                            parent.remove(child)

            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")
            view.arch_base = new_xml

    def remove_field_view(self):
        views = self.env['ir.ui.view'].search([('model', '=', self.model_id.model)])
        for view in views:
            parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
            root = ET.fromstring(view.arch_base, parser=parser)
            for parent in root.iter():
                children = list(parent)
                for i, child in enumerate(children):
                    if child.tag == "field" and child.attrib.get("name") == self.name:
                        parent.remove(child)

            ET.indent(root, space="    ")
            new_xml = ET.tostring(root, encoding="unicode")
            view.arch_base = new_xml

    def write(self, vals):
        is_comment = False
        if "name" in vals:
            new_name = vals['name']
            for record in self:
                old_name = record.name
                if 'name' in vals and old_name != new_name:
                    record.comment_field_view(new_name, old_name)
                    is_comment = True
        result = super(IrModelFields, self).write(vals)

        for record in self:
            if 'name' in vals and is_comment:
                record.uncomment_field_view()

        return result

    @api.onchange('compute')
    def _onchange_compute(self):
        for record in self:
            fus = ["PRODUCT(", "SUM(", "MINUS("]
            compute = record.compute
            if compute:
                if any(word in compute for word in fus):
                    normalized = compute.replace("'", '"')

                    start = normalized.find('("')
                    end = normalized.rfind('")')

                    fields_part = normalized[start + 2:end]
                    depends = fields_part.replace(':', ', ')

                    if record.depends != depends:
                        record.depends = depends
                elif "SUM_COL(" in compute:
                    record.depends = self.get_sum_col_depends(compute)
                elif "SUM_COL" in record.compute:
                    pass
            else:
                record.depends = False

    def get_sum_col_depends(self, compute_str):
        if not compute_str:
            return False

        compute_normalized = compute_str.replace("'", '"')

        if "SUM_COL(" not in compute_normalized:
            return False

        start = compute_normalized.find('(')
        end = compute_normalized.rfind(')')
        params = compute_normalized[start + 1:end]

        matches = re.findall(r'"(.*?)"', params)
        if len(matches) >= 2:
            return matches[1]
        return False

    def unlink(self):
        for record in self:
            record.remove_field_view()

        return super(IrModelFields, self).unlink()
