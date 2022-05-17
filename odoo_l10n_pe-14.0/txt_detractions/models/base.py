from odoo import api, fields, models
from ..reports.report_detractions import ReportInvBalTxt
from odoo.exceptions import UserError, ValidationError
import base64


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    reference_invoice = fields.Many2one(
        string='Factura Referencia',
        comodel_name='account.move',
        domain="[('partner_id', '=', partner_id), ('payment_state', 'in', ('paid', 'partial', 'in_payment'))]"
    )
    detractions_constancy_number = fields.Char(string='Número de constancia')
    journal_temporal = fields.Char(related='journal_id.name')

    tempora_accmov = fields.Many2many('account.move', string="Temporal Account Move", store=True)

    def calculate_detractions(self):
        account_move = self.reference_invoice
        discount_percentage = False
        # We look for if there is a l10n_pe_withhold_percentage not false
        for lines in account_move.invoice_line_ids:
            if lines.product_id.l10n_pe_withhold_percentage:
                discount_percentage = lines.product_id.l10n_pe_withhold_percentage
                break
        if not discount_percentage:
            return
        else:
            if account_move.currency_id.name == 'PEN':
                self.amount = round(account_move.amount_total * (discount_percentage / 100))
            else:
                self.amount = account_move.amount_total * (discount_percentage / 100)

    @api.onchange('detractions_constancy_number')
    def update_account_move_from_account_payment(self):
        if self.batch_payment_id and (
                self.batch_payment_id.state == 'reconciled' or self.batch_payment_id.state == 'sent') and self.journal_id.name == 'Detracciones':
            self.env['account.move'].search([('name', '=', self.tempora_accmov.name)]).update({'voucher_number': self.detractions_constancy_number,
                                                                                               'voucher_payment_date': self.batch_payment_id.date})
        if self.batch_payment_id and (
                self.batch_payment_id.state == 'reconciled' or self.batch_payment_id.state == 'sent') and self.journal_id.name == 'Autodetracción':
            self.env['account.move'].search([('name', '=', self.reference_invoice.name)]).update({'voucher_number': self.detractions_constancy_number,
                                                                                                  'voucher_payment_date': self.batch_payment_id.date})


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    lot_number = fields.Char(string='Número de lote')
    journal_temporal = fields.Char(related='journal_id.name')

    txt_filename = fields.Char(string='Filaname .txt')
    txt_binary = fields.Binary(string='Reporte .TXT')
    payment_ids = fields.One2many(readonly=False)

    def generate_detraction(self):
        amount_total = 0
        for payment in self.payment_ids:
            if payment.currency_id.name == 'PEN':
                amount_total = amount_total + payment.amount
            else:
                amount_not_PEN_total = 0
                for acc_move in payment.move_id.line_ids:
                    amount_not_PEN_total = acc_move.credit or acc_move.debit
                amount_total = amount_total + amount_not_PEN_total
        amount_total = str(round(amount_total)) + '.00'

        if self.journal_id.name == 'Detracciones':
            bank_nation = False
            line_data = {
                '01': '*',
                'ruc': self.env.company.vat,
                'name': self.env.company.name,
                'lot_number': self.lot_number,
                'total_amount': amount_total
            }

            list_data = []
            for obj_line in self.payment_ids:
                obj_line.tempora_accmov = obj_line.reconciled_bill_ids
                for bank in obj_line.partner_id.bank_ids:
                    if bank.bank_id.bic == 'BANCPEPL':
                        bank_nation = (bank.acc_number).replace('-', '')

                if obj_line.currency_id.name == 'PEN':
                    values = {
                        'ruc': obj_line.partner_id.vat,
                        'selection_ids': obj_line.reconciled_bill_ids.invoice_line_ids[0].product_id.l10n_pe_withhold_code,
                        'bank': bank_nation,
                        'amount': str(obj_line.amount),
                        'operation_type': obj_line.reconciled_bill_ids.operation_type_detraction,
                        'invoice_date': obj_line.reconciled_bill_ids.invoice_date,
                        'document_type': obj_line.reconciled_bill_ids.l10n_latam_document_type_id.code,
                        'ref': obj_line.reconciled_bill_ids.ref
                    }
                    list_data.append(values)
                else:
                    for acc_mov in obj_line.move_id.line_ids:
                        if acc_mov.account_id.user_type_id.name == 'Activos Circulantes':
                            amount_not_PEN = acc_mov.credit or acc_mov.debit
                            amount_not_PEN = round(amount_not_PEN)
                    values = {
                        'ruc': obj_line.partner_id.vat,
                        'selection_ids': obj_line.reconciled_bill_ids.invoice_line_ids[0].product_id.l10n_pe_withhold_code,
                        'bank': bank_nation,
                        'amount': str(amount_not_PEN) + '.00',
                        'operation_type': obj_line.reconciled_bill_ids.operation_type_detraction,
                        'invoice_date': obj_line.reconciled_bill_ids.invoice_date,
                        'document_type': obj_line.reconciled_bill_ids.l10n_latam_document_type_id.code,
                        'ref': obj_line.reconciled_bill_ids.ref
                    }
                    list_data.append(values)
        elif self.journal_id.name == 'Autodetracción':
            for bank in self.env.company.partner_id.bank_ids:
                if bank.bank_id.bic == 'BANCPEPL':
                    bank_nation = (bank.acc_number).replace('-', '')
            line_data = {
                '01': 'P',
                'ruc': self.env.company.vat,
                'name': self.env.company.name,
                'lot_number': self.lot_number,
                'total_amount': amount_total
            }
            list_data = []
            for obj_line in self.payment_ids:
                if not obj_line.reference_invoice:
                    raise UserError("Usted debe seleccionar una factura de referencia para que pueda generar su txt."
                                    "Deberá ir al módulo de pagos y seleccionar su factura de referencia")
                else:
                    if obj_line.currency_id.name == 'PEN':
                        values = {
                            'ruc': obj_line.partner_id.vat,
                            'selection_ids': obj_line.reference_invoice.invoice_line_ids[0].product_id.l10n_pe_withhold_code,
                            'bank': bank_nation,
                            'amount': str(obj_line.amount),
                            'operation_type': obj_line.reference_invoice.operation_type_detraction,
                            'invoice_date': obj_line.reference_invoice.invoice_date,
                            'document_type': obj_line.reference_invoice.l10n_latam_document_type_id.code,
                            'ref': obj_line.reference_invoice.name.replace(' ', '')
                        }
                        list_data.append(values)
                    else:
                        for acc_mov in obj_line.move_id.line_ids:
                            if acc_mov.account_id.user_type_id.name == 'Activos Circulantes':
                                amount_not_PEN = acc_mov.credit or acc_mov.debit
                                amount_not_PEN = round(amount_not_PEN)
                        values = {
                            'ruc': obj_line.partner_id.vat,
                            'selection_ids': obj_line.reference_invoice.invoice_line_ids[0].product_id.l10n_pe_withhold_code,
                            'bank': bank_nation,
                            'amount': str(amount_not_PEN) + '.00',
                            'operation_type': obj_line.reference_invoice.operation_type_detraction,
                            'invoice_date': obj_line.reference_invoice.invoice_date,
                            'document_type': obj_line.reference_invoice.l10n_latam_document_type_id.code,
                            'ref': obj_line.reference_invoice.name.replace(' ', '')
                        }
                        list_data.append(values)

        else:
            return

        data_name = {
            'vat': self.env.company.vat,
            'lot_number': self.lot_number
        }
        report_txt = ReportInvBalTxt(data_name, line_data, list_data)

        values_content = report_txt.get_content()

        data = {
            'txt_binary': base64.b64encode(values_content.encode() or '\n'.encode()),
            'txt_filename': report_txt.get_filename(),
        }
        self.write(data)
        return


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    journal_temporal = fields.Char(related='journal_id.name')

    def calculate_detraction_register(self):
        self.ensure_one()
        line = self.line_ids._origin
        account_move = line.move_id
        discount_percentage = False
        for lines in account_move.invoice_line_ids:
            if lines.product_id.l10n_pe_withhold_percentage:
                discount_percentage = lines.product_id.l10n_pe_withhold_percentage
                break
        if not discount_percentage:
            return
        else:
            if account_move.currency_id.name == 'PEN':
                self.amount = round(account_move.amount_total * (discount_percentage / 100))
            else:
                self.amount = account_move.amount_total * (discount_percentage / 100)
            return {
                'name': 'Register Payment',
                'context': self.env.context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.payment.register',
                'res_id': self.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
