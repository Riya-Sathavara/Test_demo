# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    flight_book_id = fields.Many2one('flight.booking', string='Flight Booking')
    hotel_book_id = fields.Many2one('hotel.booking', string='Hotel Booking')