# -*- coding: utf-8 -*-
# from odoo import http


# class personalAttendance(http.Controller):
#     @http.route('/personal_attendance/personal_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/personal_attendance/personal_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('personal_attendance.listing', {
#             'root': '/personal_attendance/personal_attendance',
#             'objects': http.request.env['personal_attendance.personal_attendance'].search([]),
#         })

#     @http.route('/personal_attendance/personal_attendance/objects/<model("personal_attendance.personal_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('personal_attendance.object', {
#             'object': obj
#         })
