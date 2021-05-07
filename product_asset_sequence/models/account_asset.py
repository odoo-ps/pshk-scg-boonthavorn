from odoo import models, fields, api, _


class AccountAsset(models.Model):
    _inherit = "account.asset"

    asset_running_number = fields.Char(string='Asset Running number')

    @api.model
    def create(self, vals):
        vals['asset_running_number'] = self.env['ir.sequence'].next_by_code('account.asset')
        return super(AccountAsset, self).create(vals)
