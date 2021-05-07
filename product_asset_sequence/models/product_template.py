from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"
    product_running_number = fields.Char(string="Product Running Number")


    @api.model
    def create(self, vals):
        seq, p_type = self.env['ir.sequence'], vals['type']
        num = None
        if p_type == "product":
            num = seq.next_by_code('product.template.storable')
        elif p_type == "service":
            num = seq.next_by_code('product.template.service')
        elif p_type == "consu":
            num = seq.next_by_code('product.template.consumable')
        vals['product_running_number'] = num
        return super(ProductTemplate, self).create(vals)
