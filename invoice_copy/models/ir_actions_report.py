# -*- coding: utf-8 -*-

from odoo import models

class PurchaseOrder(models.Model):
    _inherit = 'ir.actions.report'

    def _get_original_account_moves(self, res_ids):
        watched_report_names = [
            'point_of_sale.report_invoice',
            'account.report_invoice',
            'account.report_invoice_with_payments',
        ]
        if res_ids and self.report_name in watched_report_names:
            records = self.env[self.model].browse(res_ids)
            # else self.model is account.move so record is already an account.move
            if self.model == 'pos.order':
                records = records.account_move
            return records.filtered(lambda r: r.state == 'posted' and r.x_report_is_copy is False)
        return self.env['account.move']

    def _render_qweb_pdf(self, res_ids=None, data=None):
        # if you pass data to a report it removes the id from the url...
        if data and data.get('is_copy'):
            res_ids = self._context.get('active_ids')
        res = super()._render_qweb_pdf(res_ids, data)
        original_moves = self._get_original_account_moves(res_ids)
        if original_moves and self.model == 'account.move' and not self._context.get('is_copy'):
            original_moves.x_report_is_copy = True
            # Save a copy of the record as attachment not the original
            super(PurchaseOrder, self.with_context(attachment_copy=original_moves.ids))._render_qweb_pdf(original_moves.ids, data)
        return res

    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        unsave_ids = self._context.get('attachment_copy')
        if unsave_ids:
            original_moves = self.env['account.move'].browse(unsave_ids)
            for move in original_moves:
                if move.id in save_in_attachment:
                    self.sudo().retrieve_attachment(move).unlink()
                    del save_in_attachment[move.id]
        res = super()._post_pdf(save_in_attachment, pdf_content, res_ids)
        return res
