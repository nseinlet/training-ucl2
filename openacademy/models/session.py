# -*- coding: utf-8 -*-
from openerp import models, fields, api

 
class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
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