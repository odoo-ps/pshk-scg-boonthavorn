from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    x_po_percent_discount = fields.Float(string='Percent Discount', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    @api.onchange('x_po_percent_discount')
    def _onchange_x_percent_discount(self):
        for line in self.order_line:
            line.x_line_percent_discount = self.x_po_percent_discount
