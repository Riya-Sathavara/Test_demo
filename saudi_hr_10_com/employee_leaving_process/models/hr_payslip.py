# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    eos_id = fields.Many2one('end.of.service.benefit', string='End Of Service Benefit')
    add_eos = fields.Boolean(string='Add EOS', default=False)
    lines_total = fields.Float(compute='_compute_payslip_total_pay', string='Total Pay')
    
    @api.multi
    def _compute_payslip_total_pay(self):
        for payslip in self:
            total = 0.0
            for line in payslip.line_ids:
                if line.code == 'NET':
                    total = line.total
            payslip.lines_total = total
            
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.eos_id = False
        self.add_eos = False
        eos_search = self.env['end.of.service.benefit'].search([('employee_id','=',self.employee_id.id), ('state','=','approved')], limit=1)
        if eos_search:
            self.eos_id = eos_search.id
            
    @api.multi
    def compute_sheet(self):
        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            #delete old payslip lines
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
            lines = [(0, 0, line) for line in self.get_payslip_lines(contract_ids, payslip.id)]
              
            #Add new line for EOS amount if you want to add eos amount for employee
            #if any EOS created for emploee the Add eos boolean will automatically visible for related employee.
            #if you want to add eos just check add eos boolean and compute sheet.
            if payslip.add_eos:
                rule = self.env.ref('employee_leaving_process.hr_salary_rule_eos')
                #Create new end of service line.
                eos_line = (0,0, {
                        'salary_rule_id': rule.id,
                        'contract_id': payslip.contract_id.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'condition_select': rule.condition_select,
                        'condition_python': rule.condition_python,
                        'condition_range': rule.condition_range,
                        'condition_range_min': rule.condition_range_min,
                        'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        'amount_percentage_base': rule.amount_percentage_base,
                        'register_id': rule.register_id.id,
                        'amount': payslip.eos_id.eos,
                        'employee_id': payslip.employee_id.id,
                        'quantity': 1.0,
                        'rate': 100
                    })
                #add End of servicxe benefit amount into net amount as this is allowance for employee
                for line in lines:
                    if line[2].get('code') == 'NET':
                        line[2].update({'amount' : line[2].get('amount') + payslip.eos_id.eos})
                lines.append(eos_line)
            payslip.write({'line_ids': lines, 'number': number})
        return True
        
