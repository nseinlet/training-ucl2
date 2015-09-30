# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import timedelta
 
class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(compute="_compute_end_date", inverse="_compute_inverse_end_date", store=True)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=['|', ('instructor', '=', True), ('category_id.name', 'like', 'Teacher')])
    course_id = fields.Many2one('openacademy.course', string='Course')
    attendee_ids = fields.Many2many('res.partner', string="Attendees", relation="openacademy_inscription", column1="session_id", column2="partner_id")
    inscription_ids = fields.Many2one('openacademy.inscription', "session_id")
    taken_seats = fields.Integer('%age of seats', compute='_compute_taken_seats')
    active = fields.Boolean(default=True)
    
    @api.depends('attendee_ids', 'seats')
    def _compute_taken_seats(self):
        for rec in self:
            if rec.seats==0:
                rec.taken_seats=0
            else:
                rec.taken_seats = 100 * len(rec.attendee_ids) / rec.seats
                
    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.duration:
                rec.end_date = fields.Datetime.from_string(rec.start_date) + timedelta(days=rec.duration, seconds=-1)
    
    @api.onchange('end_date')
    def _compute_inverse_end_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.duration = (fields.Datetime.from_string(rec.end_date) - fields.Datetime.from_string(rec.start_date)).days + 1

    @api.onchange('attendee_ids', 'seats')
    def _onchange_seats(self):
        if self.seats<0:
            return {
                    'warning': {
                            'title': '# of seats',
                            'message': 'No negative number of seats',
                }
            }
        elif self.seats<len(self.attendee_ids):
            return {
                    'warning': {
                            'title': '# of seats',
                            'message': 'Not enough seats',
                }
            }
            
    @api.constrains('instructor_id', 'attendee_ids')
    def _const_instructor(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id.id in rec.attendee_ids.ids:
                raise ValidationError("Instructor cannot be an attendee of his own session")
            