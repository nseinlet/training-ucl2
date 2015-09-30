# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string="Is instructor")
    session_ids = fields.Many2many('openacademy.session', string="Sessions", relation="openacademy_inscription", column2="session_id", column1="partner_id")
    inscription_ids = fields.One2many('openacademy.inscription', "partner_id")