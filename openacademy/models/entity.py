# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Entity(models.Model):
    _name = 'openacademy.entity'
    
    name=fields.Char(required=True)
    parent_id = fields.Many2one('openacademy.entity', string="Parent entity")
    child_ids = fields.One2many('openacademy.entity', 'parent_id')
    parent_left = fields.Integer()
    parent_right = fields.Integer()
    
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
    