# -*- coding: utf-8 -*-


from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # ---------- Fields management

    slip_id = fields.Many2one('hr.payslip', string='Payslip')
