# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    payment_method_id = fields.Many2one('account.payment.method', string='Método de pago',
                                        domain=[('payment_type', '=', 'inbound')])

    @api.depends('payment_type', 'journal_id', 'payment_method_id')
    def _compute_payment_method_line_fields(self):
        super(AccountPaymentRegister, self)._compute_payment_method_line_fields()
        for wizard in self:
            if wizard.payment_method_id:
                payment_method_lines = wizard.available_payment_method_line_ids.filtered(
                    lambda pml: pml.payment_method_id == wizard.payment_method_id
                )
                wizard.available_payment_method_line_ids = payment_method_lines
                wizard._compute_payment_method_line_id()
                if wizard.payment_method_line_id.id not in wizard.available_payment_method_line_ids.ids:
                    wizard.hide_payment_method_line = False
                else:
                    wizard.hide_payment_method_line = len(wizard.available_payment_method_line_ids) == 1 \
                                                      and wizard.available_payment_method_line_ids.code == 'manual'

    @api.depends('payment_type', 'journal_id', 'payment_method_id')
    def _compute_payment_method_line_id(self):
        super(AccountPaymentRegister, self)._compute_payment_method_line_id()
        for wizard in self:
            if wizard.available_payment_method_line_ids and wizard.payment_method_id:
                payment_method_lines = wizard.available_payment_method_line_ids.filtered(
                    lambda pml: pml.payment_method_id == wizard.payment_method_id
                )
                wizard.payment_method_line_id = payment_method_lines[0]._origin if payment_method_lines else None
            else:
                wizard.payment_method_line_id = False
