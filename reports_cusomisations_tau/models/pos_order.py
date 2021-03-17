# -*- coding: utf-8 -*-

from odoo import api, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders, draft=False):
        res = super(PosOrder, self).create_from_ui(orders, draft)
        for i in res:
            for j in orders:
                if j['data']['name'] == i['pos_reference']:
                    related_order = self.env['pos.order'].search([('id','=', i['id'])])
                    related_order.session_id.config_id.x_custom_sequence_number = j['data']['x_custom_sequence_number']
        return res
