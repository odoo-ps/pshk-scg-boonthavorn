from odoo import models, fields


class PurchseOrder(models.Model):
    _inherit = "purchase.order"

    x_po_approver = fields.Many2one('hr.employee', string="PO Approver")
    x_last_lock_date = fields.Datetime('Last Lock Date', readonly=1, copy=False)

    def button_approve(self, force=False):
        self = self.filtered(lambda order: order._approval_allowed())
        self.write({'state': 'purchase', 'date_approve': fields.Datetime.now(), 'x_last_lock_date': fields.Datetime.now()})
        self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        return {}

    def button_done(self):
        self.write({'state': 'done', 'priority': '0', 'x_last_lock_date': fields.Datetime.now()})
