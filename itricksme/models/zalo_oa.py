# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, datetime
from odoo.exceptions import UserError



class ZaloOa(models.Model): 

    _name = 'zalo.oa'
    _description = 'zalo.oa'
    _rec_name = 'name'
    _order = 'name desc'

    name = fields.Char(string='Name', required=True)
    ma_phieu = fields.Char(string='Mã phiếu',readonly=True, default=lambda self: 'New')
    
    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New' == 'New'):
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('maphieu.code') or 'New'
            res = super(ZaloOa, self).create(vals)
        return res
