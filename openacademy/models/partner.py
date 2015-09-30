# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string="Is instructor")