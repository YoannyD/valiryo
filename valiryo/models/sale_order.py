# -*- coding: utf-8 -*-
# © 2020 Ingetive - <info@ingetive.com>

import re
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    sale_country_id = fields.Many2one("res.country", string="País pedido")
    marketplace = fields.Boolean("Marketplace")
    transferencia_bancaria = fields.Boolean("Transferencia bancaria")
    bank_id = fields.Many2one('res.partner.bank', string='Cuenta bancaria', check_company=True)
    company_partner_id = fields.Many2one("res.partner", compute="_compute_company_partner", 
                                         string="Contacto compañia")
    importe_euros = fields.Monetary("Importe base €", compute="_compute_importe_euros", store = True)
    
    
    @api.onchange('partner_id')
    def _onchange_partner_id_warning(self):
        res = super(SaleOrder, self)._onchange_partner_id_warning()
        if not self.partner_id:
            return res
        
        self = self.with_company(self.company_id)
        if self.partner_id.bank_id:
            self.bank_id = self.partner_id.bank_id.id
            
        self.transferencia_bancaria = self.partner_id.transferencia_bancaria
        return res
    
    def _compute_company_partner(self):
        for r in self:
            r.company_partner_id = self.env.company.partner_id.id
            
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'transferencia_bancaria': self.transferencia_bancaria,
            'partner_bank_id': self.bank_id.id
        })
        return invoice_vals
    
    @api.depends("amount_untaxed", "date_order")
    def _compute_importe_euros(self):
        for r in self:
            rate = 0
            if r.date_order:
                euro = self.env['res.currency.rate'].search([
                    ('company_id', '=', r.company_id.id),
                    ('currency_id', '=', r.currency_id.id),
                    ('name', '<=', r.date_order.strftime('%Y-%m-%d'))
                ], limit = 1)
                if euro:
                    rate = 1/euro.rate
            importe_original = r.amount_untaxed
            r.update({'importe_euros': importe_original * rate})
            # Si no tasa para Euro el importe_validacion_euros sera igual a 0