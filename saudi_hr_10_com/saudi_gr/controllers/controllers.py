# -*- coding: utf-8 -*-
from odoo import http

# class SaudiGr(http.Controller):
#     @http.route('/saudi_gr/saudi_gr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/saudi_gr/saudi_gr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('saudi_gr.listing', {
#             'root': '/saudi_gr/saudi_gr',
#             'objects': http.request.env['saudi_gr.saudi_gr'].search([]),
#         })

#     @http.route('/saudi_gr/saudi_gr/objects/<model("saudi_gr.saudi_gr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('saudi_gr.object', {
#             'object': obj
#         })