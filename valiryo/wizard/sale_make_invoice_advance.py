# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    
    def _create_invoice(self, order, so_line, amount):
        _logger.warning("_create_invoice")
        return super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
    
    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        res.update({
            'transferencia_bancaria': order.transferencia_bancaria,
            'partner_bank_id': order.bank_id.id,
            'payment_method_id': order.payment_method_id.id or None,
        })
        return res
        
    