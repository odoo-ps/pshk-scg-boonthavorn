# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    x_number_sequence = fields.Char(string='Partner sequence number:')
    x_partner_type = fields.Selection([('customer', 'Customer'), ('vendor', 'Vendor'), ('affiliates', 'Affiliates'), ('employee', 'Employee'), ('others', 'Others')], default='customer', string="Partner type")
    x_credit_limit_is_invisible = fields.Boolean(compute='_compute_show_credit_limit', store=True)

    @api.depends('property_payment_term_id')
    def _compute_show_credit_limit(self):
        payment_term_immediate = self.env.ref('account.account_payment_term_immediate')
        for rec in self:
            if rec.property_payment_term_id == payment_term_immediate:
                rec.x_credit_limit_is_invisible = True
            else:
                rec.x_credit_limit_is_invisible = False

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
