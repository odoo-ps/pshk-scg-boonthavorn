# -*- coding: utf-8 -*-

from odoo import models, fields, _

from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'account.move'

    x_report_is_copy = fields.Boolean("Original report is printed", groups="account.group_account_manager")


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    def _print_document(self):
        action = super()._print_document()
        action['context'].update({'is_copy': True})
        # if you do not pass extra data the context is not modified...
        action['data'] = {'is_copy': True}
        return action
