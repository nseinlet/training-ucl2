# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Course(models.Model):
    _name = 'openacademy.course'
    _inherit = 'mail.thread'
    
    name = fields.Char(required=True, track_visibility="always")
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', string="Responsible", track_visibility="on_change")
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    entity_id = fields.Many2one('openacademy.entity')
    entity2_id = fields.Many2one('openacademy.entity', domain="[('id', 'child_of', entity_id), ('id', '!=', entity_id)]")
    
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)
    
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]