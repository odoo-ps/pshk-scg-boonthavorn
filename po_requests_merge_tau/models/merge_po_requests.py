# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_merge_po_requests(self):
        """
            merge same vendor po requests
        """
        # check all are in RFQ status
        if not all(purchase_order.state == "draft" for purchase_order in self):
            raise UserError(_('Only RFQ can be merged'))

        # check more than 1 po requests selected
        if len(self) < 2:
            raise UserError(_('Please select more than 1 purchase order from the same vendor.'))

        # check all are from the same vendor
        vendor = self[0].partner_id
        if not all(vendor == purchase_order.partner_id for purchase_order in self):
            raise UserError(_('Vendor should be the same.'))

        # check all are from same picking_type_id
        picking_type_id = self[0].picking_type_id
        if not all(picking_type_id == purchase_order.picking_type_id for purchase_order in self):
            raise UserError(_('Operation type should be the same.'))

        # start merging
        merged_po = self.env['purchase.order'].create({
            'partner_id': vendor.id,
            'origin': ', '.join([rec.origin for rec in self if rec.origin ]),
            'picking_type_id': picking_type_id.id,
        })

        not_to_merge_lines_ids = []
        for purchase_order in self:
            if not purchase_order.origin: # can merge the sale order lines
                for line in purchase_order.order_line:
                    target_line_to_merge = merged_po.order_line.filtered(lambda x: x.product_id == line.product_id and x.id not in not_to_merge_lines_ids)
                    if target_line_to_merge:
                        target_line_to_merge.product_qty += line.product_qty
                    else:
                        line.write({'order_id': merged_po.id})
            else: # do not merge the sale order lines, append them
                not_to_merge_lines_ids += purchase_order.order_line.ids
                purchase_order.order_line.write({'order_id': merged_po.id})

        # add log note in the chatter
        message_string = ""
        for purchase_order in self:
            message_string += "<a href=# data-oe-model=purchase.order data-oe-id=%d>%s</a> " % (
                            purchase_order.id, purchase_order.name)

        message_body = _("Merged from orders %s") % (message_string)

        merged_po.message_post(body=message_body)

        # cancel old orders
        self.button_cancel()

        # return window action in edit mode
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create new po',
            'res_model': 'purchase.order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': merged_po.id,
        }
