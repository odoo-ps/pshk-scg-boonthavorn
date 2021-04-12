from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    x_pos_id = fields.Text(string="POS ID")
    x_payment_term = fields.Text(string="Payment Term")
    x_custom_sequence_prefix = fields.Text(string="Custom Sequence Prefix")
    x_custom_sequence_number = fields.Integer(string="Custom Sequence Nubmer", help='A custom session-unique sequence number for the order', default=1, readonly=1)
    x_khr_currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('id', '=', 66)]))
    x_rate = fields.Float(related='x_khr_currency_id.rate', store=True, readonly=True)
    x_symbol = fields.Char(related='x_khr_currency_id.symbol', store=True, readonly=True)
