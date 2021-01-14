from odoo import api, fields, models, _
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

        #start merging
        merged_po = self.env['purchase.order'].create({
            'partner_id': vendor.id
        })

        self.mapped('order_line').write({'order_id': merged_po.id})

        #add log note in the chatter
        message_body = "Merged from orders "
        for purchase_order in self:
            message_body = message_body + "<a href=# data-oe-model=purchase.order data-oe-id=%d>%s</a> " % (
                       purchase_order.id, purchase_order.name)

        merged_po.message_post(body=message_body)

        #cancel old orders
        self.button_cancel()

        #return window action in edit mode
        return {
                'type': 'ir.actions.act_window',
                'name': 'Create new po',
                'res_model': 'purchase.order',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': merged_po.id,
                }
