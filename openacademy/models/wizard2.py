# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Wizard2(models.TransientModel):
    _name = 'openacademy.wizard2'
    
    state = fields.Selection( (('step1', 'Step 1'), ('step2', 'Step 2')) , default="step1")
    session_id = fields.Many2one('openacademy.session',
        string="Session", required=True)
    country_id = fields.Many2one('res.country')
    
    @api.multi
    def step2(self):
        self.state = 'step2'
        return {
            'name': 'Wizard 2',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'openacademy.wizard2',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }