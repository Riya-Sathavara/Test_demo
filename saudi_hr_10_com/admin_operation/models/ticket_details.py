# -*- coding: utf-8 -*-

from odoo import fields, models, api

@api.model
def action_button(model, state):
    model.ensure_one()
    model.write({'state': state})
    
class TicketDetails(models.Model):
    _name = 'ticket.details'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char('Ticket Type', required=True)
    travel_purpose_id = fields.Many2one('travel.purpose', string='Traveling Purpose')
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange', required=True)
    employee_code = fields.Char('Employee Code', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    office = fields.Char('Office')
    no_person = fields.Integer('No. of Person', required=True)
    start_date = fields.Date('Preferred Start Date', required=True)
    travel_from = fields.Char(string='Country From', required=True)
    travel_to = fields.Char(string='Country To', required=True)
    traveling_date_from = fields.Date('Traveling From Date', required=True)
    traveling_date_to = fields.Date('Traveling To Date', required=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approval', 'Waiting for approval'), ('validate', 'Validate'), ('approved', 'Approved'), ('refuse', 'Refuse'), ('cancel', 'Cancel')],default='draft', string='State')
    description = fields.Text('Description')
    hr_expense_ids = fields.One2many('hr.expense', 'flight_booking_id', string='Expense')
    ir_attachment_ids = fields.One2many('ir.attachment', 'flight_book_id', string='Expense')
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'waiting_for_approval':
            return 'admin_operation.mt_ticket_details_confirmed'
        elif 'state' in init_values and self.state == 'validate':
            return 'admin_operation.mt_ticket_details_validated'
        elif 'state' in init_values and self.state == 'approved':
            return 'admin_operation.mt_ticket_details_approved'
        elif 'state' in init_values and self.state == 'refuse':
            return 'admin_operation.mt_ticket_details_refused'
        elif 'state' in init_values and self.state == 'cancel':
            return 'admin_operation.mt_ticket_details_canceled'
        return super(TicketDetails, self)._track_subtype(init_values)
    
    def add_followers(self, employee):
        user_ids = []
        if employee.sudo().user_id:
            user_ids.append(employee.sudo().user_id.id)
        if employee.sudo().department_id and employee.sudo().department_id.manager_id:
            user_ids.append(employee.sudo().department_id.manager_id.user_id.id)
        self.sudo().message_subscribe_users(user_ids=user_ids)     
    
    @api.model
    def default_get(self, fields):
        rec = super(TicketDetails, self).default_get(fields)
        employee = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        rec.update({'employee_id': employee.id})
        return rec
    
    @api.multi
    def name_get(self):
        result = []
        if self.employee_id:
            name = self.employee_id.name  +  ','  +  self.start_date
            result.append((self.id, name))
        return result
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
        return super(TicketDetails, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(int(vals.get('employee_id')))
            vals.update({'job_id': employee.job_id.id, 'department_id': employee.department_id.id, 'employee_code': employee.employee_code})
            self.add_followers(employee)
        return super(TicketDetails, self).write(vals)
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.employee_code = self.employee_id.employee_code
        self.write({'department_id': self.employee_id.department_id.id, 'name': self.employee_id.id})
        self.job_id = self.employee_id.job_id
        self.department_id = self.employee_id.department_id
        
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