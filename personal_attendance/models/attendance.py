# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Attendance(models.Model):
     _inherit = "hr.attendance"

     netto_workingtime = fields.Float(string='Nettoarbeitszeit')
#     _name = 'personal_attendance.personal_attendance'
#     _description = 'personal_attendance.personal_attendance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
