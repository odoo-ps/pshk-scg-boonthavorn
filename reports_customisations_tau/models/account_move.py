from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    x_cashier = fields.Char(string="Cashier")
    x_approved_by = fields.Char(string="Approved by")
