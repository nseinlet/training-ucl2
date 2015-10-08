# -*- coding: utf-8 -*-
from openerp import http

class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('openacademy.my_awesome_index', {
            'teachers': http.request.env['res.partner'].sudo().search([('instructor', '=', True)]),
        })

    @http.route('/openacademy/teacher/<model("res.partner"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('openacademy.biography', {
            'person': teacher
        })
        
#     @http.route('/openacademy/openacademy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openacademy.listing', {
#             'root': '/openacademy/openacademy',
#             'objects': http.request.env['openacademy.openacademy'].search([]),
#         })

#     @http.route('/openacademy/openacademy/objects/<model("openacademy.openacademy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openacademy.object', {
#             'object': obj
#         })