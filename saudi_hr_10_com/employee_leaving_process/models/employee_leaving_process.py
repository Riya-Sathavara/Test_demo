# -*- coding: utf-8 -*-
#Manage Below List of Class Here.
#EmployeeEquipment
#EmployeeDocument
#EmployeeLeavingProcess
#EmployeeClearanceProcess
#EndOfServiceBenefit

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from chameleon.nodes import Domain

@api.model
def action_button(model, state):
    model.ensure_one()
    model.write({'state': state})
    
class EmployeeEquipment(models.Model):
    _inherit = 'employee.equipment'
    
    elp_id = fields.Many2one('employee.leaving.process', string='Employee Leaving Process')
    ecp_id = fields.Many2one('employee.clearance.process', string='Employee Clearance Process')
    
class EmployeeDocument(models.Model):
    _inherit = 'employee.document'
    
    elp_id = fields.Many2one('employee.leaving.process', string='Employee Leaving Process')
    ecp_id = fields.Many2one('employee.clearance.process', string='Employee Clearance Process')
    
class Holidays(models.Model):
    _inherit = "hr.holidays"
    
    @api.onchange('holiday_status_id')
    def _onchange_leave_type(self):
        domain = []
        domain = [('company_id', '=', self.env.ref('base.main_company').id)]
    
    
class EmployeeLeavingProcess(models.Model):
    _name = 'employee.leaving.process'
    _rec_name= 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    leave_reason = fields.Text('Leaving Reason')
    handle_by = fields.Many2one('hr.employee', string='Handle By')
    office = fields.Char('Office')
    requested_date = fields.Date('Requested Date', required=True, default=fields.Date.context_today)
    notice_start_date = fields.Date('Notice Start Date', required=True)
    notice_end_date = fields.Date('Notice End Date', required=True)
    equipment_ids = fields.One2many('employee.equipment', 'elp_id', string='Equipment Lines')
    document_ids = fields.One2many('employee.document', 'elp_id', string='Equipment Lines')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('refuse', 'Refuse'), ('cancel', 'Cancel')], track_visibility='onchange',default='draft', string='State')
    
    _sql_constraints = [
        ('employee_leaving_process_unique', 'unique (employee_id)', 'The Employee Leaving Process must be unique per employee !')
    ]
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'employee_leaving_process.mt_employee_leaving_process_waiting_for_approved'
        elif 'state' in init_values and self.state == 'validate':
            return 'employee_leaving_process.mt_employee_leaving_process_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'employee_leaving_process.mt_employee_leaving_process_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'employee_leaving_process.mt_employee_leaving_process_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'employee_leaving_process.mt_employee_leaving_process_canceled'
        return super(EmployeeLeavingProcess, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        print "_______employee___", employee
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        
#          if employee.sudo().handle_by:
#              user_ids.append(employee.sudo().handle_by.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(EmployeeLeavingProcess, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 
                         'department_id': employee.department_id.id, 
                         'employee_code': employee.employee_code, 
                         'equipment_ids': [(6, 0, [eq.id for eq in employee.equipment_ids])],
                         'document_ids': [(6, 0, [eq.id for eq in employee.document_ids])]})
        return super(EmployeeLeavingProcess, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 
                         'department_id': employee.department_id.id, 
                         'employee_code': employee.employee_code, 
                         'equipment_ids': [(6, 0, [eq.id for eq in employee.equipment_ids])],
                         'document_ids': [(6, 0, [eq.id for eq in employee.document_ids])]})
        return super(EmployeeLeavingProcess, self).write(vals)
    
    @api.multi
    def action_confirm(self):
        self.add_followers(self.employee_id)
        action_button(self, 'waiting_for_approval')
        self.confirmed_by = self.env.uid
        self.confirmed_date = fields.Datetime.now()
        
    @api.multi
    def action_approve(self):
        action_button(self, 'approved')
        self.approved_by = self.env.uid
        self.approved_date = fields.Datetime.now()
        emp_cler_obj = self.env['employee.clearance.process']
#          On validate state start employee clearance process.
        vals = {'employee_id': self.employee_id.id,
                'leave_reason': self.leave_reason,
                'handle_by': self.handle_by.id,
                'office': self.office,
                'requested_date': self.requested_date,
                'notice_start_date': self.notice_start_date,
                'notice_end_date': self. notice_end_date,
                'equipment_ids': [(6, 0, [eq.id for eq in self.employee_id.equipment_ids])],
                'document_ids': [(6, 0, [eq.id for eq in self.employee_id.document_ids])],
                'state': 'draft'
                }
        emp_cler_obj.create(vals)
        
    @api.multi
    def action_validate(self):
        action_button(self, 'validate')
        self.validate_by = self.env.uid
        self.validate_date = fields.Datetime.now()
        
    @api.multi
    def action_refuse(self):
        action_button(self, 'refuse')
        
    @api.multi
    def action_cancel(self):
        action_button(self, 'cancel')
        
    @api.multi
    def action_draft(self):
        action_button(self, 'draft')
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.employee_code = self.employee_id.employee_code
        self.job_id = self.employee_id.job_id
        self.department_id = self.employee_id.department_id
        self.equipment_ids = [(6, 0, [eq.id for eq in self.employee_id.equipment_ids])]
        self.document_ids = [(6, 0, [doc.id for doc in self.employee_id.document_ids])]


class EmployeeClearanceProcess(models.Model):
    _name = 'employee.clearance.process'
    _rec_name= 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    leave_reason = fields.Text('Leaving Reason')
    handle_by = fields.Many2one('hr.employee', string='Handle By')
    office = fields.Char('Office')
    requested_date = fields.Date('Requested Date', required=True)
    notice_start_date = fields.Date('Notice Start Date', required=True)
    notice_end_date = fields.Date('Notice End Date', required=True)
    equipment_ids = fields.One2many('employee.equipment', 'ecp_id', string='Equipment Lines')
    document_ids = fields.One2many('employee.document', 'ecp_id', string='Equipment Lines')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('refuse', 'Refuse'), ('cancel', 'Cancel')], track_visibility='onchange',default='draft', string='State')

    _sql_constraints = [
        ('employee_clearance_process_unique', 'unique (employee_id)', 'The Employee Clearance Process must be unique per employee !')
    ]
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'employee_leaving_process.mt_employee_clearance_process_waiting_for_approved'
        elif 'state' in init_values and self.state == 'validate':
            return 'employee_leaving_process.mt_employee_clearance_process_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'employee_leaving_process.mt_employee_clearance_process_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'employee_leaving_process.mt_employee_clearance_process_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'employee_leaving_process.mt_employee_clearance_process_canceled'
        return super(EmployeeClearanceProcess, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        if employee.sudo().handle_by:
            user_ids.append(employee.sudo().handle_by.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(EmployeeClearanceProcess, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 
                         'department_id': employee.department_id.id, 
                         'employee_code': employee.employee_code,
                         'equipment_ids': [(6, 0, [eq.id for eq in employee.equipment_ids])],
                         'document_ids': [(6, 0, [eq.id for eq in employee.document_ids])]})
        return super(EmployeeClearanceProcess, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 
                         'department_id': employee.department_id.id, 
                         'employee_code': employee.employee_code,
                         'equipment_ids': [(6, 0, [eq.id for eq in employee.equipment_ids])],
                         'document_ids': [(6, 0, [eq.id for eq in employee.document_ids])]})
        return super(EmployeeClearanceProcess, self).write(vals)
    
    @api.multi
    def action_confirm(self):
        self.add_followers(self.employee_id)
        action_button(self, 'waiting_for_approval')
        self.confirmed_by = self.env.uid
        self.confirmed_date = fields.Datetime.now()
        
    @api.multi
    def action_approve(self):
        action_button(self, 'approved')
        self.approved_by = self.env.uid
        self.approved_date = fields.Datetime.now()
        emp_eos_obj = self.env['end.of.service.benefit']
        payslip_obj = self.env['hr.payslip']
#          On Approved state start employee EOS process.
        vals = {'employee_id': self.employee_id.id,
                'state': 'draft',
                }
        eos = emp_eos_obj.create(vals)
        for slip in self.employee_id.slip_ids:
            slip.write({'eos_id': eos.id})
        
    @api.multi
    def action_validate(self):
        action_button(self, 'validate')
        self.validate_by = self.env.uid
        self.validate_date = fields.Datetime.now()
        
    @api.multi
    def action_refuse(self):
        action_button(self, 'refuse')
        
    @api.multi
    def action_cancel(self):
        action_button(self, 'cancel')
        
    @api.multi
    def action_draft(self):
        action_button(self, 'draft')
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.employee_code = self.employee_id.employee_code
        self.job_id = self.employee_id.job_id
        self.department_id = self.employee_id.department_id
        self.equipment_ids = [(6, 0, [eq.id for eq in self.employee_id.equipment_ids])]
        self.document_ids = [(6, 0, [doc.id for doc in self.employee_id.document_ids])]


class EndOfServiceBenefit(models.Model):
    _name = 'end.of.service.benefit'
    _rec_name= 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    @api.multi
    @api.depends('employee_id', 'date_of_joining')
    def _get_years(self):
        for eos in self:
            today = datetime.now()
            #convert string date format to datetime format
            if eos.date_of_joining:
                joining = datetime.strptime(eos.date_of_joining, "%Y-%m-%d")
                #find experience based on joining date
                rdelta = relativedelta(today, joining)
                eos.exp_year = rdelta.years
                eos.exp_month = rdelta.months

    @api.multi
    @api.depends('employee_id', 'exp_year', 'exp_month')
    def _get_eos_amount(self):
        for eos in self:
            self.env.cr.execute("SELECT wage FROM hr_contract WHERE date_end=(SELECT MAX(date_end) FROM hr_contract WHERE employee_id=%s) and employee_id=%s", (eos.employee_id.id, eos.employee_id.id))
            contract = self.env.cr.fetchone() or False
            if contract:
                # If employee experience is lesthen 5 and morethan 2 year then his last salary *no of year experience* 16.67%( which is 1/3 divide by 2 is half salary).
                # (Basic * years) *16.67%
                wage = contract[0]
                if eos.exp_year >=2 and eos.exp_year < 5 :
                    eos.eos = wage * eos.exp_year * 0.1667
                # if Employee has more than 5 and less then 10 year experience he will get half salary for first five year and full salary in rest of years.
                # ((Basic * 5/2) + (basic * rest_years)) * 66.67%
                elif eos.exp_year >=5 and eos.exp_year <10:
                    year = eos.exp_year - 5
                    eos.eos = ((wage * 5 / 2) + (wage*year)) * 0.6667
                # if employee has more then 10 year experience then he will getr first five year half salary and rest of year he will eligible for full salary 
                # ((Basic*5/2) + (basic * rest_of_years)) * 100%
                elif eos.exp_year >=10:
                    year = eos.exp_year - 5
                    eos.eos = ((wage * 5/2) + (wage*year))

    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    date_of_joining = fields.Date(related='employee_id.date_of_joining', string="Joining Date", readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    eos = fields.Float(compute='_get_eos_amount', string='EOS', help='Compute EOS amount as per saudi rule')
    payslip_ids = fields.One2many('hr.payslip', 'eos_id', string='Payslip Lines')
    exp_year = fields.Integer(compute='_get_years', string='Experience', readonly=True)
    exp_month = fields.Integer(compute='_get_years', string='No of Months', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('refuse', 'Refuse'), ('cancel', 'Cancel')], track_visibility='onchange',default='draft', string='State')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'employee_leaving_process.mt_end_of_service_benefit_waiting_for_approved'
        elif 'state' in init_values and self.state == 'validate':
            return 'employee_leaving_process.mt_end_of_service_benefit_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'employee_leaving_process.mt_end_of_service_benefit_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'employee_leaving_process.mt_end_of_service_benefit_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'employee_leaving_process.mt_end_of_service_benefit_canceled'
        return super(EndOfServiceBenefit, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(EndOfServiceBenefit, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.multi
    @api.constrains('employee_id')
    def _check_for_contract(self):
        eos_search = self.search([('employee_id', '=', self.employee_id.id),('state', 'not in', ['cancel'])])
        error_message = ""
        if len(eos_search) > 1:
            error_message = ('The End of Service Benefit must be unique per employee !.\nOr cancel old EOS.\n')
        for eos in self:
            self.env.cr.execute("SELECT wage FROM hr_contract WHERE date_end=(SELECT MAX(date_end) FROM hr_contract WHERE employee_id=%s)", (eos.employee_id.id,))
            contract = self.env.cr.fetchone() or False
            if not contract:
                error_message += ('No contract found for employee %s.')%(eos.employee_id.name)
        if error_message:
            raise ValidationError(_(error_message))
    
    @api.model
    def create(self, vals):
        employee = False
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 
                         'department_id': employee.department_id.id, 
                         'employee_code': employee.employee_code,
                        #'payslip_ids': [(6, 0, [slip.id for slip in self.employee_id.slip_ids])]
                         })
        res = super(EndOfServiceBenefit, self).create(vals)
        if employee:
            for slip in employee.slip_ids:
                slip.write({'eos_id': res.id})
        return res
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 
                         'department_id': employee.department_id.id, 
                         'employee_code': employee.employee_code,
#                           'payslip_ids': [(6, 0, [slip.id for slip in self.employee_id.slip_ids])]
                         })
            for slip in self.employee_id.slip_ids:
                slip.write({'eos_id': self.id})
        return super(EndOfServiceBenefit, self).write(vals)
    
    @api.multi
    def action_confirm(self):
        self.add_followers(self.employee_id)
        action_button(self, 'waiting_for_approval')
        
    @api.multi
    def action_approve(self):
        action_button(self, 'approved')
        
    @api.multi
    def action_validate(self):
        action_button(self, 'validate')
        
    @api.multi
    def action_refuse(self):
        action_button(self, 'refuse')
        
    @api.multi
    def action_cancel(self):
        action_button(self, 'cancel')
        
    @api.multi
    def action_draft(self):
        action_button(self, 'draft')
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.employee_code = self.employee_id.employee_code
        self.job_id = self.employee_id.job_id
        self.department_id = self.employee_id.department_id
#          self.payslip_ids = [(6, 0, [slip.id for slip in self.employee_id.slip_ids])]
        