from odoo import models, api, fields, _
from odoo.tools.safe_eval import safe_eval, datetime, dateutil, time
from odoo.exceptions import ValidationError


SAFE_EVAL_BASE = {
    'datetime': datetime,
    'dateutil': dateutil,
    'time': time,
}

def sum_c(self, name, range2):
    fields = range2.split(':')

    for record in self:
        total = 0
        for field in fields:
            total += record[field] or 0
        record[name] = total

def minus_c(self, name, range2):
    fields = range2.split(':')

    for record in self:
        total = record[fields[0]] or 0
        for field in fields[1:]:
            total -= record[field] or 0
        record[name] = total

def product_c(self, name, range2):
    fields = range2.split(':')

    for record in self:
        total = 1
        for field in fields:
            total *= record[field] or 0
        record[name] = total

def sum_col(self, name, sum_field, relation):

    for record in self:
        total = record[relation].mapped(sum_field)
        record[name] = sum(total)

def fnc(self, name, lb):

    for record in self:
        record[name] = lb(record)

def make_compute_patched(field_name, text, deps):

    def func(self):
        ctx = SAFE_EVAL_BASE.copy()
        ctx.update({
            'self': self,
            'SUM': lambda range2: sum_c(self, field_name, range2),
            'MINUS': lambda range2: minus_c(self, field_name, range2),
            'PRODUCT': lambda range2: product_c(self, field_name, range2),
            'SUM_COL': lambda sum_field, relation: sum_col(self, field_name, sum_field, relation),
            'SET': lambda lb: fnc(self, field_name, lb),
        })
        return safe_eval(text, ctx, mode="exec")

    deps = [d.strip() for d in deps.split(",")] if deps else []
    return api.depends(*deps)(func)

class IrModelFields(models.Model):
    _inherit = ["ir.model.fields", 'mail.thread']

    ttype2 = fields.Selection(
        selection=[
                ('char', _('char')),
                ('text', _('text')),
                ('integer', _('integer')),
                ('float', _('float')),
                ('boolean', _('boolean')),
                ('date', _('date')),
                ('datetime', _('datetime')),
                ('selection', _('selection')),
                ('many2one', _('many2one')),
                ('one2many', _('one2many')),
                ('many2many', _('many2many')),
                ('reference', _('reference')),
                ('html', _('html')),
                ('binary', _('binary')),
                ('monetary', _('monetary')),
        ],
        string='Field Type',
        required=True
    )

    @api.onchange('ttype2')
    def _onchange_ttype2(self):
        for record in self:
            if record.ttype2:
                record.ttype = record.ttype2

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "ttype" in vals and not vals.get("ttype2", False):
                vals['ttype2'] = vals['ttype']
        return super(IrModelFields, self).create(vals_list)

    def write(self, vals):
        if "ttype2" in vals and vals['ttype2'] != vals['ttype']:
            vals['ttype'] = vals['ttype2']

        result = super(IrModelFields, self).write(vals)

        return result

    def _instanciate_attrs(self, field_data):
        attrs = super(IrModelFields, self)._instanciate_attrs(field_data=field_data)

        if field_data['compute']:
            attrs['compute'] = make_compute_patched(field_data["name"], field_data['compute'], field_data['depends'])

        return attrs

class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    def _get_eval_context(self, action=None):
        eval_context = super()._get_eval_context(action=action)
        record = eval_context.get('record')

        eval_context.update({
            'SEARCH_READ': lambda model_name=False, **args: self.search_read_data(model_name, **args),
            'CREATE': lambda model_name=False, data=None: self.create_record(data, model_name=model_name),
            'WRITE': lambda id, data, model_name=False: self.write_record(id, data, model_name=model_name),
            "DELETE": lambda model_name, domain=False: self.delete_records(model_name, domain),
            'CREATE_OR_WRITE': lambda model_name, fields, data, key=False, condition=True: self.create_or_write(model_name, fields, data, key, condition),
            "EXPAND_ARRAY": lambda model_name, map_str, domain=False: self.expand_array(model_name, map_str, domain, record),
            "ACT_WINDOW": lambda model_name: self.get_act_window(model_name),
            "UNIQUE_MODEL": lambda name: self.get_model(name),
            "DISPLAY_SEQUENCE" : lambda: self.display_sequence(record),
            "REF_ID" : f"{record._name},{record.id}" if record else False,
            "REF" : lambda model, id: f"{model},{id}",
        })
        return eval_context
    
    def get_act_window(self, model_name):
        model = self.get_model(model_name)

        return {
            "type": "ir.actions.act_window",
            "name": model._description,
            "res_model": model._name,
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "new"
        }

    def display_sequence(self, record):
        sequence = self.env['ir.sequence'].search([('code', '=', record._name)], limit=1)
        if sequence:
            record.write({"x_name": sequence.get_next_char(sequence.number_next_actual)})

    def get_model(self, model_name):
        t = self.env["ir.model"].search([('name', '=', model_name)], limit=1)
        return self.env[t.model] if t else None
    
    def delete_records(self, model_name, domain):
        model = self.get_model(model_name)
        records = model.search(domain)
        records.unlink()

    def expand_array(self, model_name, map_str, domain2, record=None):
        data = {
            k.strip(): v.strip()
            for k, v in (p.split(":", 1) for p in map_str.split(","))
        }
        value = data.get("value")
        multi = data.get("multi")
        before = data.get("before")

        domain = []
        order = "id"
        fields = [value]

        if multi:
            fields.append(multi)
        if before:
            domain.append((before, '<', record[before]))
            order = f"{before}, id"
        if domain2:
            for v in domain2:
                domain.append(v)

        lines = self.get_model(model_name).search_read(
            domain=domain,
            fields=fields,
            order=order
        )
        arr = []

        for line in lines:
            a = line[value]
            c = [a]
            if multi:
                b = int(line[multi])
                c = [a * b / abs(b)] * abs(b)

            arr.extend(c)

        return arr

    def search_read_data(self, model_name=False, **args):
        if not model_name:
            model_name = self.model_id.name

        model = self.get_model(model_name)
        return model.search_read(**args)

    def write_record(self, id, data, model_name=False):
        if not model_name:
            model_name = self.model_id.name

        record = self.get_model(model_name).browse(id)
        record.write(data)

    def create_record(self, data, model_name=False):
        if not model_name:
            model_name = self.model_id.name

        model = self.get_model(model_name)
        return model.create(data)

    def create_or_write(self, model_name, fields, values, key=False, condition=True):
        model = self.get_model(model_name)

        domain = []
        clear_domain = []
        for field in fields.split(','):
            field = field.strip()
            domain.append((field, '=', values.get(field)))

            if not key:
                continue

            if field in list(map(str.strip, key.split(","))):
                clear_domain.append((field, '!=', values.get(field)))
            else:
                clear_domain.append((field, '=', values.get(field)))

        records = model.search(domain)
        clear_records = model.search(clear_domain)

        if clear_records:
            clear_records.unlink()

        if not condition:
            records.unlink()
        elif records:
            records.write(values)
        else:
            records = model.create(values)
        return records

class IrActionsAct_window(models.Model):
    _inherit = 'ir.actions.act_window'

    def open(self):
        return self.read()[0]
