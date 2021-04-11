from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_price_unit(self):
        """ Returns the unit price to value this stock move """
        self.ensure_one()
        price_unit = self.price_unit
        self.price_unit = self.purchase_line_id._get_discounted_price_unit()
        res = super()._get_price_unit()
        self.price_unit = price_unit
        return res
