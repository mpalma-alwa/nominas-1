from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
import pytz
import logging
import urllib.request
import urllib.parse

_logger = logging.getLogger(__name__)


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _action_sbs_currency_update(self):
        url = 'http://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx'
        try:
            open_html = urllib.request.urlopen(url)
            html = BeautifulSoup(open_html, "lxml")
            tr_dollar = html.find("tr", id="ctl00_cphContent_rgTipoCambio_ctl00__0")
            currency = self.env.ref('base.USD')
            if tr_dollar and currency:
                tds_dollar = tr_dollar.findAll("td", {"class": "APLI_fila2"})
                if tds_dollar:
                    values = {
                        'compra': float(tds_dollar[0].text.strip()),
                        'venta': float(tds_dollar[1].text.strip()),
                    }
                    rate_date = fields.Datetime.now().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(self.env.user.tz or 'UTC')) + relativedelta(days=1)
                    currency_rate = self.env['res.currency.rate']
                    rate = currency_rate.search([
                        ('currency_id', '=', currency.id),
                        ('name', '=', rate_date.date()),
                        ('company_id', '=', self.env.user.company_id.id)
                    ], limit=1)

                    if not rate:
                        currency_rate.create({
                            'currency_id': currency.id,
                            'rate': 1.0 / values['venta'],
                            'name': rate_date,
                        })
                    else:
                        rate.write({
                            'rate': 1.0 / values['venta'],
                            'name': rate_date,
                        })
        except urllib.error.HTTPError as http_error:
            _logger.warning('Error: {}'.format(http_error))
        except urllib.error.URLError as url_error:
            _logger.warning('Error: {}'.format(url_error))
        except Exception as exception_error:
            _logger.warning('Error: {}'.format(exception_error))
