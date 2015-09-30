# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Inscription(models.Model):
    _name = 'openacademy.inscription'
    
    partner_id = fields.Many2one('res.partner')
    session_id = fields.Many2one('openacademy.session')
    inscription_date = fields.Date(string="Inscription date")
    