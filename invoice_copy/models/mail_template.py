# -*- coding: utf-8 -*-

from odoo import models

class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def generate_email(self, res_ids, fields):
        if self.model != 'account.move':
            return super().generate_email(res_ids, fields)

        records_uncopy = self.env[self.model].browse(res_ids).filtered(lambda r: not r.x_report_is_copy)
        records_uncopy.x_report_is_copy = True
        result = super().generate_email(res_ids, fields)
        records_uncopy.x_report_is_copy = False

        return result
