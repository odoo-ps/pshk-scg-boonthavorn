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
            'partner_id': vendor.id
        })

        # # check if order line has a sale_order_id in selected PO
        # if self.mapped('order_line.sale_line_id'):

        # self[0].mapped('order_line').write({'order_id': merged_po.id}) # merge the first purchase order

        for purchase_order in self: # loop remaining purchase order
            for line in purchase_order.order_line:
                print(line.id)
                print(merged_po.order_line.ids)
                if line.product_id in [merged_line.product_id for merged_line in merged_po.order_line]: # if have same product
                    if line.sale_order_id: # append the order line
                        line.write({'order_id': merged_po.id})
                    else: # add the quantity
                        target_line = merged_po.order_line.filtered(lambda x: x.product_id == line.product_id)
                        if target_line:
                            target_line.product_qty = target_line.product_qty + line.product_qty
                else: # append the order line
                    line.write({'order_id': merged_po.id})

        # else: #add the quantity
        #     self.mapped('order_line').write({'order_id': merged_po.id})

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
