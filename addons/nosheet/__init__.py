from . import models

from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry
from odoo.service import db
from .hash_file import build_hash_map

def post_load():
    db_names = db.list_dbs()

    for db_name in db_names:
        try:
            registry = Registry(db_name)

            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})

                current = build_hash_map()

                message = "\n".join(
                    f"{h}  {p}" for p, h in sorted(current.items())
                )

                env["ir.logging"].sudo().create({
                    "name": "integrity",
                    "type": "server",
                    "level": "info",
                    "dbname": db_name,
                    "message": message,
                    "path": "startup",
                    "func": "post_load",
                    "line": "0",
                })

                cr.commit()

        except Exception:
            pass

def post_init_hook(env):
    env.cr.execute("""
        UPDATE ir_model_fields
        SET ttype2 = ttype
        WHERE ttype2 IS NULL
    """)
