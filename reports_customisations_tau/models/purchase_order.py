from odoo import models, fields


class PurchseOrder(models.Model):
    _inherit = "purchase.order"

    x_po_approver = fields.Many2one('hr.employee', string="PO Approver")
    x_last_lock_date = fields.Datetime('Last Lock Date', readonly=1, copy=False)

    def button_approve(self, force=False):
        super(PurchseOrder, self).button_approve(force)
        self.write({'x_last_lock_date': fields.Datetime.now()})
        return {}

    def button_done(self):
        super(PurchseOrder, self).button_done()
        self.write({'x_last_lock_date': fields.Datetime.now()})
