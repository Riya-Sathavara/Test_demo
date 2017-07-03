# -*- coding: utf-8 -*-
from odoo import http

# class HrPayrollCommission(http.Controller):
#     @http.route('/hr_payroll_commission/hr_payroll_commission/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_payroll_commission/hr_payroll_commission/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_payroll_commission.listing', {
#             'root': '/hr_payroll_commission/hr_payroll_commission',
#             'objects': http.request.env['hr_payroll_commission.hr_payroll_commission'].search([]),
#         })

#     @http.route('/hr_payroll_commission/hr_payroll_commission/objects/<model("hr_payroll_commission.hr_payroll_commission"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_payroll_commission.object', {
#             'object': obj
#         })