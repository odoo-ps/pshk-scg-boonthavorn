# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class Partner(models.Model):
    _inherit = 'res.partner'

    x_number_sequence = fields.Char(string='Partner sequence number:')
    x_partner_type = fields.Selection([('customer', 'Customer'), ('vendor', 'Vendor')], default='customer', require="True", string="Partner type")


    @api.model
    def create(self, vals):
        if 'x_partner_type' in vals and 'x_number_sequence' in vals:
            if vals['x_partner_type'] == 'customer':
                vals['x_number_sequence'] = self.env['ir.sequence'].next_by_code('customer.number')
            else:
                vals['x_number_sequence'] = self.env['ir.sequence'].next_by_code('vendor.number')
            return super(Partner, self).create(vals)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_percent_discount = fields.Float(string='Percent Discount')
    x_amount_discount = fields.Monetary(compute='_amount_all', string='Amount Discount', store=True)


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

            #calculate the amount discount
            order.x_amount_discount = -(order.x_percent_discount/100 * amount_untaxed)

            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + order.x_amount_discount + amount_tax,
            })


    def action_confirm(self):
        if self.sudo().partner_id.total_due >= self.partner_id.credit_limit:
            raise UserError("You cannot confirm this sales order due to customer's overdue is over credit limit.")
        return super(SaleOrder, self).action_confirm()
