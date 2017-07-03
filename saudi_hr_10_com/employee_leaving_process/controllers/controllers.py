# -*- coding: utf-8 -*-
from odoo import http

# class EmployeeLeavingProcess(http.Controller):
#     @http.route('/employee_leaving_process/employee_leaving_process/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_leaving_process/employee_leaving_process/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_leaving_process.listing', {
#             'root': '/employee_leaving_process/employee_leaving_process',
#             'objects': http.request.env['employee_leaving_process.employee_leaving_process'].search([]),
#         })

#     @http.route('/employee_leaving_process/employee_leaving_process/objects/<model("employee_leaving_process.employee_leaving_process"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_leaving_process.object', {
#             'object': obj
#         })