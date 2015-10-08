# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import timedelta
 
class Session(models.Model):
    _name = 'openacademy.session'
    _order = 'sequence,name'
    _inherit = 'ir.needaction_mixin'
    
    name = fields.Char(required=True)
    sequence = fields.Integer(index=True)
    priority = fields.Selection((('0', 'low'), ('1', 'medium'), ('2', 'high'), ('3', 'nuclear')), default='0')
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
    hours = fields.Float(string="Duration in hours",
                         compute='_compute_hours', inverse='_compute_inverse_hours')
    attendees_counts = fields.Integer(compute='_compute_attendees_count', store=True)
    color = fields.Integer()
    state = fields.Selection((('draft', 'Draft'),
                              ('in_progress', 'In progress'),
                              ('done', 'Done')),
                             string = "State", default='draft',
                             )
    country_id = fields.Many2one('res.country', string="Country", related="instructor_id.country_id")
    
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

    @api.depends('duration')
    def _compute_hours(self):
        for rec in self:
            rec.hours = rec.duration * 24

    def _compute_inverse_hours(self):
        for rec in self:
            rec.duration = rec.hours / 24
    
    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        for rec in self:
            rec.attendees_counts = len(rec.attendee_ids)
            
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
            
    @api.multi
    def set_draft(self):
        for rec in self:
            rec.state = 'draft'
            
    @api.one
    def set_in_progress(self):
        self.state = 'in_progress'
        
    @api.multi
    def set_done(self):
        self.write({'state': 'done'})
        
    @api.multi
    def attendees_list(self):
        return {
            'name': 'Students',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'domain': [['id', 'in', self.attendee_ids.ids]],
        }
        
    @api.multi
    def launch_wizard2(self):
        wiz = self.env['openacademy.wizard2'].create({
            'session_id': self.id,
        })
        wiz.country_id = self.env['res.country'].search([('name' , 'ilike', 'fr')])[0]
        
        return {
            'name': 'Wizard 2',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'openacademy.wizard2',
            'res_id': wiz.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        
    @api.model
    def _needaction_domain_get(self):
        return [('taken_seats', '>=', 80)]
    