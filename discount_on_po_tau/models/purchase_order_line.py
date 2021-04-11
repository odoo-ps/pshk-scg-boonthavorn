from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    x_line_percent_discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)

    def _get_discounted_price_unit(self):
        return self.price_unit * (1- self.x_line_percent_discount/100)

    @api.onchange('product_id')
    def onchange_product_id(self):
        super().onchange_product_id()
        self.x_line_percent_discount = self.order_id.x_po_percent_discount

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move)
        res['discount'] = self.x_line_percent_discount
        return res

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'x_line_percent_discount')
    def _compute_amount(self):
        return super()._compute_amount()

    def _get_stock_move_price_unit(self):
        self.ensure_one()
        price_unit = self.price_unit
        self.price_unit = self._get_discounted_price_unit()
        res = super()._get_stock_move_price_unit()
        self.price_unit = price_unit
        return res

    def _prepare_compute_all_values(self):
        res = super()._prepare_compute_all_values()
        res['price_unit'] = self._get_discounted_price_unit()
        return res
