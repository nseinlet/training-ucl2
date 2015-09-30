# -*- coding: utf-8 -*-
from openerp import models, fields, api

 
class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=['|', ('instructor', '=', True), ('category_id.name', 'like', 'Teacher')])
    course_id = fields.Many2one('openacademy.course', string='Course')
    attendee_ids = fields.Many2many('res.partner', string="Attendees", relation="openacademy_inscription", column1="session_id", column2="partner_id")
    inscription_ids = fields.Many2one('openacademy.inscription', "session_id")