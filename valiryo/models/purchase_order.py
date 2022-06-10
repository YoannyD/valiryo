# -*- coding: utf-8 -*-
# © 2020 Ingetive - <info@ingetive.com>

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _prepare_invoice(self):
        invoice_values = super(PurchaseOrder, self)._prepare_invoice()
        if self.partner_id and self.partner_id.payment_mode_id:
            invoice_values['payment_mode_id'] = self.partner_id.payment_mode_id
        return invoice_values
