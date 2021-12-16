# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    bank_id = fields.Many2one("res.partner.bank", company_dependent=True, string="Cuenta bancaria")
    transferencia_bancaria = fields.Boolean("Transferencia bancaria")
    company_partner_id = fields.Many2one("res.partner", compute="_compute_company_partner", 
                                         string="Contacto compañia")
    
    def _compute_company_partner(self):
        for r in self:
            r.company_partner_id = self.env.company.partner_id.id
    


