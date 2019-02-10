# -*- coding: utf-8 -*-
from odoo import http

# class Salaire(http.Controller):
#     @http.route('/salaire/salaire/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salaire/salaire/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salaire.listing', {
#             'root': '/salaire/salaire',
#             'objects': http.request.env['salaire.salaire'].search([]),
#         })

#     @http.route('/salaire/salaire/objects/<model("salaire.salaire"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salaire.object', {
#             'object': obj
#         })