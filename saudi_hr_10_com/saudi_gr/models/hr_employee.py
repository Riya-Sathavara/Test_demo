# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Employee(models.Model):
    _inherit = 'hr.employee'
    
    gosi_no = fields.Char('Gosi No.')
