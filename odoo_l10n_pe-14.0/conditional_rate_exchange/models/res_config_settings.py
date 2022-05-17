from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    live_currency_sync = fields.Boolean(
        string='NO Sync'
    )

    def _parse_xe_com_data(self, available_currencies):
        if self.live_currency_sync:
            return {}
        else:
            return super(ResCompany, self)._parse_xe_com_data(available_currencies)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    live_currency_sync = fields.Boolean(
        related="company_id.live_currency_sync",
        readonly=False,
        help='If this field is checked, the exchange rate will not be synced via the native Odoo query to xe.com'
    )
