from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_price_unit(self):
        """ Returns the unit price to value this stock move """
        self.ensure_one()
        price_unit = self.purchase_line_id._get_discounted_price_unit()
        # If the move is a return, use the original move's price unit.
        if self.origin_returned_move_id and self.origin_returned_move_id.sudo().stock_valuation_layer_ids:
            price_unit = self.origin_returned_move_id.stock_valuation_layer_ids[-1].unit_cost
        return not self.company_id.currency_id.is_zero(price_unit) and price_unit or self.product_id.standard_price
