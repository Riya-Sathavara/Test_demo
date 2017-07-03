# -*- coding: utf-8 -*-

# Equipment
# EmployeeEquipment
# EquipmentRequest
# EmployeeRegistration
# EmployeeDeregistration

from odoo import models, fields, api

@api.model
def action_button(model, state):
    model.ensure_one()
    model.write({'state': state})
    
class Equipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    type = fields.Selection([('hardware', 'Hardware'), ('software', 'Software')], default = 'hardware', string='Type', required=True)
    
class EmployeeEquipment(models.Model):
    _name = 'employee.equipment'
    
    employee_id = fields.Many2one('hr.employee', string='Employee')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment',required=True)
    type = fields.Selection(related='equipment_id.type')
    approved_by = fields.Many2one('hr.employee', string='Approve By',required=True)
    approved_date = fields.Date(string='Approve Date')
    remark = fields.Text(string='Remark')
    status = fields.Selection([('yes', 'Yes'), ('na', 'N/A')], default='yes')
    
class EmployeeDocument(models.Model):
    _name = 'employee.document'
    
    name = fields.Char(string='Document name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    submit_date = fields.Date(string='Submit Date')
    remark = fields.Text(string='Remark')
    status = fields.Selection([('yes', 'Yes'), ('na', 'N/A')], default='yes')

class EquipmentRequest(models.Model):
    _name = 'equipment.request'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    type = fields.Selection([('hardware', 'Hardware'), ('software', 'Software')], default = 'hardware', string='Type', required=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', required=True)
    description = fields.Text('Description')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('cancel', 'Cancel'), ('refuse', 'Refuse')], track_visibility='onchange',default='draft', string='State')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_it.mt_equipment_request_waiting_for_approved'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_it.mt_equipment_request_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_it.mt_equipment_request_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_it.mt_equipment_request_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_it.mt_equipment_request_canceled'
        return super(EquipmentRequest, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(EquipmentRequest, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EquipmentRequest, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EquipmentRequest, self).write(vals)
    
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
        self.env['employee.equipment'].create({'employee_id': self.employee_id.id, 
                                               'equipment_id': self.equipment_id.id,
                                               'approved_by': self.env.uid,
                                               'approved_date': fields.Datetime.now()})
        
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
        
class EmployeeRegistration(models.Model):
    _name = 'employee.registration'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    email = fields.Char('Email')
    skype = fields.Char('Skype')
    remote_access = fields.Boolean('Remote Access')
    laptop_desktop = fields.Char('Laptop/Desktop')
    serial_no = fields.Char('Serial No')
    charger = fields.Boolean('Charger')
    headphone = fields.Boolean('Headphone')
    access_card = fields.Char('Access Card')
    pendrive = fields.Boolean('Pendrive')
    carrying_case = fields.Boolean('Carrying case')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('cancel', 'Cancel'), ('refuse', 'Refuse')], track_visibility='onchange',default='draft', string='State')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_it.mt_employee_registration_waiting_for_approved'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_it.mt_employee_registration_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_it.mt_employee_registration_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_it.mt_employee_registration_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_it.mt_employee_registration_canceled'
        return super(EmployeeRegistration, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(EmployeeRegistration, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EmployeeRegistration, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EmployeeRegistration, self).write(vals)
    
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
        
class EmployeeDeregistration(models.Model):
    _name = 'employee.deregistration'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    email = fields.Char('Email')
    skype = fields.Char('Skype')
    remote_access = fields.Boolean('Remote Access')
    laptop_desktop = fields.Char('Laptop/Desktop')
    serial_no = fields.Char('Serial No')
    charger = fields.Boolean('Charger')
    headphone = fields.Boolean('Headphone')
    access_card = fields.Char('Access Card')
    pendrive = fields.Boolean('Pendrive')
    carrying_case = fields.Boolean('Carrying case')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('cancel', 'Cancel'), ('refuse', 'Refuse')], track_visibility='onchange',default='draft', string='State')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_it.mt_employee_deregistration_waiting_for_approved'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_it.mt_employee_deregistration_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_it.mt_employee_deregistration_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_it.mt_employee_deregistration_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_it.mt_employee_deregistration_canceled'
        return super(EmployeeDeregistration, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(EmployeeDeregistration, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EmployeeDeregistration, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EmployeeDeregistration, self).write(vals)
    
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
    