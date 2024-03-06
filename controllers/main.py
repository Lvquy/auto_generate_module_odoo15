# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request



class ItricksMe(http.Controller):

    @http.route(['/team'], auth='public', website=True)
    def team(self, **kw):
        return request.render('itricks_me.team')
