# -*- coding: utf-8 -*-

from odoo import fields, models, api

class HrExpenseExpense(models.Model):
    _inherit = 'hr.expense'
    
    flight_booking_id = fields.Many2one('flight.booking', string='Flight Booking')
    hotel_booking_id = fields.Many2one('hotel.booking', string='Hotel Booking')