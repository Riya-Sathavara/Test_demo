# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Employee(models.Model):
    _inherit = 'hr.employee'
    
    arabic_name = fields.Char('Arabic Name')
    employee_code = fields.Char('Employee Code')
    date_of_joining = fields.Date('Date of Joining', required=True)
