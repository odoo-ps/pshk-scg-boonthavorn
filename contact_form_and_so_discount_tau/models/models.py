# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class Partner(models.Model):
    _inherit = 'res.partner'

    x_number_sequence = fields.Char(string='Partner sequence number:')
    x_partner_type = fields.Selection([('customer', 'Customer'), ('vendor', 'Vendor'), ('affiliates', 'Affiliates'), ('employee', 'Employee'), ('others', 'Others')], default='customer', string="Partner type")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('x_partner_type', 'customer') == 'customer':
                vals['x_number_sequence'] = self.env['ir.sequence'].next_by_code('customer.number')
            elif vals.get('x_partner_type', 'vendor') == 'vendor':
                vals['x_number_sequence'] = self.env['ir.sequence'].next_by_code('vendor.number')
        return super(Partner, self).create(vals_list)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name and self.env.context.get('from_sale'):
            domain = ['&', ('x_partner_type', '!=', 'vendor'), '|', ('name', operator, name), ('x_number_sequence', operator, name)] # can be searched in SO
        elif name and self.env.context.get('from_purchase'):
            domain = ['&', ('x_partner_type', '!=', 'customer'), '|', ('name', operator, name), ('x_number_sequence', operator, name)] # can be searched in PO
        elif name:
            domain = ['|', ('name', operator, name), ('x_number_sequence', operator, name)] # can be searched in the rest
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_percent_discount = fields.Float(string='Percent Discount')
    x_amount_discount = fields.Monetary(compute='_amount_all', string='Amount Discount', store=True)
    x_customer_available_credit_limit_amount = fields.Float(compute='_calculate_customer_available_credit_limit_amount', string='Customer Available Credit Limit Balance')

    @api.depends('partner_id')
    def _calculate_customer_available_credit_limit_amount(self):
        for order in self:
            order.x_customer_available_credit_limit_amount = order.partner_id.credit_limit - order.partner_id.total_invoiced

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
            order.x_amount_discount = -(order.x_percent_discount/100 * amount_untaxed)

            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + order.x_amount_discount + amount_tax,
            })

    def action_confirm(self):
        if self.sudo().partner_id.total_due > self.partner_id.credit_limit:
            raise UserError("You cannot confirm this sales order due to customer's overdue is over credit limit.")
        return super(SaleOrder, self).action_confirm()
