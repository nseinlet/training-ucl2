# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Inscription(models.Model):
    _name = 'openacademy.inscription'
    
    name = fields.Char(compute='_get_inscription_name')
    partner_id = fields.Many2one('res.partner')
    session_id = fields.Many2one('openacademy.session')
    inscription_date = fields.Date(string="Inscription date")
    
    @api.depends('session_id', 'partner_id')    
    def _get_inscription_name(self):
        for rec in self:
            rec.name = "%s-%s" % (rec.partner_id.name if rec.partner_id else '', rec.session_id.name if rec.session_id else '')