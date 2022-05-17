from odoo import fields, models, api
from odoo.osv import expression


class ModelSunatCatalog(models.AbstractModel):
    _name = 'model.sunat.catalog'
    _description = 'Modelo catálogo de SUNAT'

    name = fields.Char(
        string='Nombre',
        compute='compute_name'
    )
    code = fields.Char(
        string='Código',
        required=True
    )
    description = fields.Char(
        string='Descripción',
        required=True
    )

    @api.depends('code', 'description')
    def compute_name(self):
        for rec in self:
            rec.name = "[%s] %s" % (rec.code or '', rec.description or '')


class IgvAfectationType(models.Model):
    _name = 'igv.afectation.type'
    _description = '[07] Tipo de Afectación al IGV'
    _inherit = 'model.sunat.catalog'


class IscCalculationSystem(models.Model):
    _name = 'isc.calculation.system'
    _description = '[08] Tipo de Sistema de Cálculo del ISC'
    _inherit = 'model.sunat.catalog'


class TransferTypeCodes(models.Model):
    _name = 'transfer.type.codes'
    _description = '[18] Códigos de modalidad de Traslado'
    _inherit = 'model.sunat.catalog'


class TransferReasonCodes(models.Model):
    _name = 'transfer.reason.codes'
    _description = '[20] Códigos de motivo de Traslado'
    _inherit = 'model.sunat.catalog'


class ChargeDiscountCodes(models.Model):
    _name = 'charge.discount.codes'
    _description = '[53] Códigos de cargos o descuentos'
    _inherit = 'model.sunat.catalog'


class AccountTax(models.Model):
    _inherit = 'account.tax'

    isc_calculation_system_id = fields.Many2one(
        comodel_name='isc.calculation.system',
        string='[08] Tipo de Sistema de Cálculo del ISC'
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_pe_charge_discount_id = fields.Many2one(
        comodel_name='charge.discount.codes',
        string='[53] Códigos de cargos o descuentos'
    )


class ClassificationServices(models.Model):
    _name = 'classification.services'
    _description = '[30] Clasificación de los bienes y servicios adquiridos'

    code = fields.Char(
        string='Código',
        required=True
    )

    description = fields.Char(
        string='Descripción',
        required=True
    )
    name = fields.Char(
        string='Descripción',
        required=True,
        related='description'
    )

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
