# -*- coding: utf-8 -*-

# Employee

from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    equipment_ids = fields.One2many('employee.equipment', 'employee_id', string='Equipment Lines')
    document_ids = fields.One2many('employee.document', 'employee_id', string='Documents')