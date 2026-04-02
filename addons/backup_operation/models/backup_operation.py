from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import os

class BackupDetail(models.Model):
    _name = "backup.detail"

    path = fields.Char(
        string="Path",
        required=True,
        readonly=True
    )
    backup_operation_id = fields.Many2one('backup.operation')

    def unlink(self):
        for record in self:
            if record.path and os.path.exists(record.path):
                try:
                    os.remove(record.path)
                except Exception as e:
                    raise ValidationError(f"Cannot delete file {record.path}")
        return super(BackupDetail, self).unlink()

class BackupOperation(models.Model):
    _name = "backup.operation"
    _description = "Backup Operation"

    nextcall = fields.Datetime("Backup starting time", required=True, default=fields.Datetime.now)
    retention = fields.Integer("Backup retention count", required=True, default=7)
    interval_number = fields.Integer("Interval Number", required=True)
    interval_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')],
        required=True,
        string="Interval Type", 
        default='days'
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('running', 'Running'),
        ('cancel', 'Cancel')],
        required=True,
        string="Status", 
        default='draft'
    )
    detail_ids = fields.One2many(
        'backup.detail', 
        'backup_operation_id',
        string="Backup details",
    )

    ref = fields.Char(string="Code", default=lambda self: _("New"))

    @api.constrains('interval_number', 'interval_type')
    def _check_interval_type_and_interval_number(self):
        for rec in self:
            if rec.interval_type == "minutes" and rec.interval_number < 15:
                raise ValidationError(f"Backup theo 'phút' phải lớn hơn 15(phút).")
            elif rec.interval_number < 1:
                raise ValidationError(f"Thời gian chạy phải lớn hơn 1.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("backup.operation")
        return super(BackupOperation, self).create(vals_list)

    def backup_db(self):
        self.ensure_one()
        from odoo.service.db import dump_db
        from datetime import datetime, timezone
        import pytz

        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now_local = datetime.now(timezone.utc).astimezone(tz).replace(microsecond=0)

        backup_path="/opt/odoo19/backups"
        backup_format="zip"
        filestore=True
        dbname = self.env.cr.dbname
        os.makedirs(backup_path, exist_ok=True)
        file_path = os.path.join(backup_path, f"{dbname}_{now_local.strftime('%d-%m-%Y_%H-%M-%S')}.{backup_format}")
        with open(file_path, "wb") as f:
            dump_db(dbname, f, backup_format, filestore)
        
        self.detail_ids.create({
            "path": file_path, 
            "backup_operation_id": self.id
        })
        if self.status != "running":
            self.status = 'running'
        return file_path

    def cleanup_old_backups(self):
        details = self.detail_ids.sorted(
            key=lambda r: r.create_date,
            reverse=True
        )

        to_delete = details[self.retention:]
        if to_delete:
            to_delete.unlink()
        
        if self.status != "running":
            self.status = 'running'
    
    def confirm_status(self):
        self.status = 'confirm'

    def cancel_status(self):
        self.status = 'cancel'

    def cron_backup(self):
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        import logging

        _logger = logging.getLogger(__name__)

        now = fields.Datetime.now()

        for record in self.search([("status", "in", ["confirm", "running"])]):
            try:
                if record.interval_type == 'minutes':
                    delta = timedelta(minutes=record.interval_number)
                elif record.interval_type == 'hours':
                    delta = timedelta(hours=record.interval_number)
                elif record.interval_type == 'days':
                    delta = timedelta(days=record.interval_number)
                elif record.interval_type == 'weeks':
                    delta = timedelta(weeks=record.interval_number)
                elif record.interval_type == 'months':
                    delta = relativedelta(months=record.interval_number)
                else:
                    continue

                next_run = record.nextcall + delta

                if now >= next_run:
                    record.backup_db()
                    record.nextcall = now

            except Exception as e:
                _logger.error(f"Cron backup failed for ID {record.id}: {str(e)}")

    def cron_cleanup_backups(self):
        for record in self.search([("status", "in", ["confirm", "running"])]):
            record.cleanup_old_backups()
