# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_percent_discount = fields.Float(string='Percent Discount')
    x_amount_discount = fields.Monetary(compute='_amount_all', string='Amount Discount', store=True)
    x_customer_available_credit_limit_amount = fields.Float(compute='_calculate_customer_available_credit_limit_amount', string='Customer Available Credit Limit Balance')

    @api.depends('partner_id')
    def _calculate_customer_available_credit_limit_amount(self):
        for order in self:
            order.x_customer_available_credit_limit_amount = order.partner_id.credit_limit - order.partner_id.total_due

    @api.depends('order_line.price_total', 'x_percent_discount')
    def _amount_all(self):

        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax

            # calculate the amount discount
            x_amount_discount = -(order.x_percent_discount/100 * amount_untaxed)
            amount_tax_after_discount = amount_tax * (1 - order.x_percent_discount/100)

            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax_after_discount,
                'amount_total': amount_untaxed + x_amount_discount + amount_tax_after_discount,
                'x_amount_discount': x_amount_discount,
            })

    def action_confirm(self):
        if self.sudo().partner_id.total_due > self.partner_id.credit_limit:
            raise UserError("You cannot confirm this sales order due to customer's overdue is over credit limit.")
        return super(SaleOrder, self).action_confirm()
