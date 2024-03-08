# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request



class ZaloOa(http.Controller):

    @http.route(['/team'], auth='public', website=True)
    def team(self, **kw):
        return request.render('itricksme.team')
