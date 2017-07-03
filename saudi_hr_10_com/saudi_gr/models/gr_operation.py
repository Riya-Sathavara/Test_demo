# -*- coding: utf-8 -*-
#Manage Below List of Class Here.
#VisaRequest
#VisaIqama
#ReligionReligion
#SponsorshipTransfer
#OtherOperation
#GrOoperations
#GrDocuments
#EmployeeGosi
# GrOperationRequiredDocument

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

@api.model
def action_button(model, state):
    model.ensure_one()
    model.write({'state': state})

class VisaRequest(models.Model):
    _name = 'visa.request'
    _rec_name= 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    email = fields.Char(related='employee_id.work_email', string='Email', readonly=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    passport_number = fields.Char('Passport Number', required=True)
    country_id = fields.Many2one('res.country', string='Nationality')
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    visa_for = fields.Selection([('individual', 'Individual'), ('family', 'Family')], string='Type', default='individual', required=True)
    visa_type = fields.Selection([('exit_re_entry', 'Exit Re-entry Visa'), ('final_exit', 'Final Exit'), ('extension_exit_re_entry', 'Extension of Exit re-entry Visa')], string='Type of Visa', required=True)
    purpose_of_visa = fields.Selection([('trainning', 'Tranning'), ('business_trip', 'Business Trip'), ('holiday', 'Holiday'),('emergency', 'Emergency'), ('other', 'Other')], string='Purpose of Visa', required=True)
    visa_number = fields.Char('VISA Number', required=True)
    visa_duration_number = fields.Integer('Visa Duration', required=True)
    visa_duration_period = fields.Selection([('month', 'Month'),('year', 'Year')], 'Visa Duration', required=True)
    visa_applied_for = fields.Many2one('res.country', string='Visa Applied for', required=True)
    departure_date = fields.Date('Departure Date', required=True)
    return_date = fields.Date('Return Date', required=True)
    approved_from_date = fields.Date('Approved Date From', required=True)
    approved_to_date = fields.Date('Approved Date To')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    description = fields.Text('Description')
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('refuse', 'Refuse'), ('cancel', 'Cancel')], track_visibility='onchange',default='draft', string='State')
    required_document = fields.Text('Required Document')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_gr.mt_visa_request_confirmed'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_gr.mt_visa_request_validated'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_gr.mt_visa_request_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_gr.mt_visa_request_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_gr.mt_visa_request_canceled'
        return super(VisaRequest, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
    
    @api.model
    def default_get(self, fields):
        rec = super(VisaRequest, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({ 'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(VisaRequest, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
            self.add_followers(employee)
        return super(VisaRequest, self).write(vals)
        
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
        
#      onchange of employee auto fill employee related data
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.employee_code = self.employee_id.employee_code
        self.passport_number = self.employee_id.passport_id
        self.country_id = self.employee_id.country_id
        self.job_id = self.employee_id.job_id
        self.department_id = self.employee_id.department_id
        
#      onchange of visa duration update applied to date field.
    @api.onchange('visa_duration_number', 'visa_duration_period')
    def onchange_visa_duration(self):
        if self.approved_from_date and self.visa_duration_number and self.visa_duration_period:
            if self.visa_duration_period == 'month':
                self.approved_to_date = fields.Date.to_string(fields.Date.from_string(self.approved_from_date) + relativedelta(months = self.visa_duration_number))
            else:
                self.approved_to_date = fields.Date.to_string(fields.Date.from_string(self.approved_from_date) + relativedelta(years = self.visa_duration_number))
        if not self.approved_from_date and self.visa_duration_number and self.visa_duration_period:
            raise UserError(_('Missing error!\n Please first fill Approved date from is required.'))
            
class VisaIqama(models.Model):
    _name = 'visa.iqama'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    iqama_type = fields.Selection([('employee', 'Employee'), ('family', 'Family'), ('new_born_baby', 'New Born Baby')], string='Iqama Type', default='employee')
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    name = fields.Char(string='Name(As In Passport)')
    arabic_name = fields.Char('Arabic Name')
    employee_code = fields.Char('Employee Code', readonly=True)
    country_id = fields.Many2one('res.country', string='Nationality')
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    office = fields.Char('Office')
    religion_id = fields.Many2one('religion.religion', string='Religion')
    birth_date = fields.Date('Date of Birth')
    profession = fields.Char('Profession')
    iqama_number = fields.Char('Iqama Number', required=True)
    serial_number = fields.Char('Serial Number', required=True)
    iqama_position = fields.Char('Iqama position', required=True)
    issue_place = fields.Char('Place of issue')
    issue_date = fields.Date('Date of issue', required=True)
    expiry_date = fields.Date('Date of Expiry', required=True)
    expiry_date_hijri = fields.Char('Date of Issue(Hijri)')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    description = fields.Text('Description')
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('cancel', 'Cancel'), ('refuse', 'Refuse')], track_visibility='onchange',default='draft', string='State')
    new_iqama = fields.Text('New Iqama Document')
    family_iqama = fields.Text('Family iqama document')
    new_baby_born_ksa_iqama = fields.Text('New born baby Iqama(in KSA)')
    new_baby_born_outside_ksa_iqama = fields.Text('New born baby Iqama (outside KSA)')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_gr.mt_visa_request_confirmed'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_gr.mt_visa_request_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_gr.mt_visa_request_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_gr.mt_visa_request_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_gr.mt_visa_request_canceled'
        return super(VisaIqama, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(VisaIqama, self).default_get(fields)
        record = self.env['gr.operation.required.document'].search([('company_id', '=', self.env.user.company_id.id)], limit=1)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'new_iqama': record.new_iqama,
                    'family_iqama': record.family_iqama,
                    'new_baby_born_ksa_iqama': record.new_baby_born_ksa_iqama,
                    'new_baby_born_outside_ksa_iqama': record.new_baby_born_outside_ksa_iqama,
                    'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(VisaIqama, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(VisaIqama, self).write(vals)
    
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
        self.arabic_name = self.employee_id.arabic_name
        self.birth_date = self.employee_id.birthday
        self.country_id = self.employee_id.country_id
        self.job_id = self.employee_id.job_id
        self.department_id = self.employee_id.department_id
    
    
class ReligionReligion(models.Model):
    _name = 'religion.religion'
    
    name = fields.Char('Religion Name', required=True)
    description = fields.Text('Religion Description')
    
    
class SponsorshipTransfer(models.Model):
    _name = 'sponsorship.transfer'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char('Sponsorship Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    manager = fields.Many2one('hr.employee', string='Manager')
    responsible_person = fields.Many2one('hr.employee', string='Responsible Person')
    description = fields.Text('Description')
    required_document = fields.Text('Required Document')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('cancel', 'Cancel'), ('refuse', 'Refuse')], track_visibility='onchange',default='draft', string='State')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_gr.mt_visa_request_confirmed'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_gr.mt_visa_request_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_gr.mt_visa_request_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_gr.mt_visa_request_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_gr.mt_visa_request_canceled'
        return super(SponsorshipTransfer, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        if employee.sudo().manager:
            user_ids.append(employee.sudo().manager.user_id.id)
        if employee.sudo().responsible_person:
            user_ids.append(employee.sudo().responsible_person.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(SponsorshipTransfer, self).default_get(fields)
        record = self.env['gr.operation.required.document'].search([('company_id', '=', self.env.user.company_id.id)], limit=1)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'required_document': record.sponsorship_transfer,'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(SponsorshipTransfer, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(SponsorshipTransfer, self).write(vals)
    
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
    
    
class OtherOperation(models.Model):
    _name = 'other.operation'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char('Operation Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    manager = fields.Many2one('hr.employee', string='Manager', required=True)
    responsible_person = fields.Many2one('hr.employee', string='Responsible Person', required=True)
    operation_id = fields.Many2one('gr.operations', string='GR Operation', required=True)
    document = fields.Text('Document')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('cancel', 'Cancel'), ('refuse', 'Refuse')], track_visibility='onchange', default='draft', string='State')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_gr.mt_visa_request_confirmed'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_gr.mt_visa_request_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_gr.mt_visa_request_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_gr.mt_visa_request_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_gr.mt_visa_request_canceled'
        return super(OtherOperation, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        if employee.sudo().manager:
            user_ids.append(employee.sudo().manager.user_id.id)
        if employee.sudo().responsible_person:
            user_ids.append(employee.sudo().responsible_person.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(OtherOperation, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(OtherOperation, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(OtherOperation, self).write(vals)
    
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
    
    
class GrOoperations(models.Model):
    _name = 'gr.operations'
    
    name = fields.Char('Operation Name', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
    
#  class GrDocuments(models.Model):
#      _name = 'gr.documents'
#      
#      name = fields.Char('Document Name', required=True)
#      operation_id = fields.Many2one('gr.operation', string='GR Operation', required=True)
#      document = fields.Text('List of Document')
#      

class EmployeeGosi(models.Model):
    _name = 'employee.gosi'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    arabic_name = fields.Char('Arabic Name')
    employee_code = fields.Char('Employee Code', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    passport_number = fields.Char('Passport Number', required=True)
    country_id = fields.Many2one('res.country', string='Nationality')
    type = fields.Selection([('saudi', 'Saudi'),('non-saudi', 'Non-Saudi')], default='saudi', string='Type', required=True)
    family_card_number = fields.Char('Family Card Number')
    issue_date = fields.Date('Issue Date')
    date_of_birth = fields.Date('Date of Birth')
    date_of_birth_hijri = fields.Char('Date of Birth(Hijri)')
    gosi_no = fields.Char('Gosi No.', required=True)
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    confirmed_date = fields.Date('Confirmed Date', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Date('Approved Date', readonly=True)
    validate_by = fields.Many2one('res.users', string='Validate By', readonly=True)
    validate_date = fields.Date('Validate Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('cancel', 'Cancel'), ('refuse', 'Refuse')], track_visibility='onchange',default='draft', string='State')
    description = fields.Text('Description')
    required_document = fields.Text('Required Document')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'saudi_gr.mt_visa_request_confirmed'
        elif 'state' in init_values and self.state == 'validate':
            return 'saudi_gr.mt_visa_request_validate'
        elif 'state' in init_values and self.state == 'approved':
            return 'saudi_gr.mt_visa_request_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'saudi_gr.mt_visa_request_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'saudi_gr.mt_visa_request_canceled'
        return super(EmployeeGosi, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)
        
    @api.model
    def default_get(self, fields):
        rec = super(EmployeeGosi, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EmployeeGosi, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(EmployeeGosi, self).write(vals)
    
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
        self.arabic_name = self.employee_id.arabic_name
        self.employee_code = self.employee_id.employee_code
        self.passport_number = self.employee_id.passport_id
        self.gosi_no = self.employee_id.gosi_no
        self.date_of_birth = self.employee_id.birthday
        self.country_id = self.employee_id.country_id
        self.job_id = self.employee_id.job_id
        self.department_id = self.employee_id.department_id
        
# Configuration for all Gr operation

class GrOperationRequiredDocument(models.Model):
    _name = 'gr.operation.required.document'
    _rec_name = 'company_id'
    
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)
    visa_request = fields.Text('Visa Request')
    new_iqama = fields.Text('New Iqama')
    family_iqama = fields.Text('Family Iqama')
    new_baby_born_ksa_iqama = fields.Text('New born baby Iqama(in KSA)')
    new_baby_born_outside_ksa_iqama = fields.Text('New born baby Iqama (outside KSA)')
    sponsorship_transfer = fields.Text('Sponsorship Transfer')
    
