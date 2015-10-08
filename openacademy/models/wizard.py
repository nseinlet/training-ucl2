# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    def _default_session(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))
    
    session_ids = fields.Many2many('openacademy.session',
        string="Session", default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    @api.multi
    def validate(self):
        #for attendee_id in self.attendee_ids:
        #    if attendee_id.id in self.session_id.attendee_ids.ids:
        #        raise ValidationError("Not the same person twice")
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        