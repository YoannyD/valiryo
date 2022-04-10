# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    required_vat = fields.Boolean("Vat requerido", default=False)
    

class AccountMove(models.Model):
    _inherit = "account.move"
    
    transferencia_bancaria = fields.Boolean("Transferencia bancaria")
    
    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if res.journal_id and res.journal_id.required_vat:
            if res.partner_id and not res.partner_id.vat:
                raise UserError(_('En este diario es obligatorio que el cliente %s tenga NIF', res.partner_id.name))
        return res
    
    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        if self.journal_id and self.journal_id.required_vat:
            if self.partner_id and not self.partner_id.vat:
                raise UserError(_('En este diario es obligatorio que el cliente %s tenga NIF', self.partner_id.name))
        return res

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

    def _get_move_display_name(self, show_ref=False):
        ''' Helper to get the display name of an invoice depending of its type.
        :param show_ref:    A flag indicating of the display name must include or not the journal entry reference.
        :return:            A string representing the invoice.
        '''
        self.ensure_one()
        name = ''
        if not self.name or self.name == '/':
            name += '(* %s)' % str(self.id)
        else:
            name += self.name
        return name + (show_ref and self.ref and ' (%s%s)' % (self.ref[:50], '...' if len(self.ref) > 50 else '') or '')