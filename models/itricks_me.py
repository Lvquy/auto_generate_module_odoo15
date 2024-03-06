# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, datetime
from odoo.exceptions import UserError



class ItricksMe(models.Model): 

    _name = 'itricks.me'
    _description = 'itricks.me'
    _rec_name = 'name'
    _order = 'name desc'

    name = fields.Char(string='Name', required=True)
    ma_phieu = fields.Char(string='Mã phiếu',readonly=True, default=lambda self: 'New')
    
    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New' == 'New'):
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('maphieu.code') or 'New'
            res = super(ItricksMe, self).create(vals)
        return res
