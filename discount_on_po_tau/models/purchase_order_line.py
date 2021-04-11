from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    x_line_percent_discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)

    def _get_discounted_price_unit(self):
        return self.price_unit * (1- self.x_line_percent_discount/100)

    @api.onchange('product_id')
    def onchange_product_id(self):
        super(PurchaseOrderLine, self).onchange_product_id()
        self.x_line_percent_discount = self.order_id.x_po_percent_discount

    @api.onchange('order_line')
    def _prepare_account_move_line(self):
        for line in self:
            line.x_line_percent_discount = self.x_line_percent_discount

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'x_line_percent_discount')
    def _compute_amount(self):
        return super(PurchaseOrderLine, self)._compute_amount()

    def _get_stock_move_price_unit(self):
        self.ensure_one()
        line = self[0]
        order = line.order_id
        price_unit = self._get_discounted_price_unit()
        if line.taxes_id:
            price_unit = line.taxes_id.with_context(round=False).compute_all(
                price_unit, currency=line.order_id.currency_id, quantity=1.0, product=line.product_id, partner=line.order_id.partner_id
            )['total_void']
        if line.product_uom.id != line.product_id.uom_id.id:
            price_unit *= line.product_uom.factor / line.product_id.uom_id.factor
        if order.currency_id != order.company_id.currency_id:
            price_unit = order.currency_id._convert(
                price_unit, order.company_id.currency_id, self.company_id, self.date_order or fields.Date.today(), round=False)
        return price_unit

    def _prepare_compute_all_values(self):
        res = super(PurchaseOrderLine, self)._prepare_compute_all_values()
        res['price_unit'] = self._get_discounted_price_unit()
        return res
