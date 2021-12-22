# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"
    
    transferencia_bancaria = fields.Boolean("Transferencia bancaria")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        self = self.with_company(self.journal_id.company_id)
        if self.partner_id.bank_id:
            self.partner_bank_id = self.partner_id.bank_id.id
            
        self.transferencia_bancaria = self.partner_id.transferencia_bancaria
        return res
    
    def action_post(self):
        for line in self.mapped('line_ids'):
            if line.account_internal_group in ['income', 'expense'] and not line.analytic_account_id:
                raise ValidationError("Es obligatorio indicar la cuenta analítica en las líneas.")
            
        res = super(AccountMove, self).action_post()
        return res