# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    slip_id = fields.Many2one('hr.payslip', string='Payslip')
