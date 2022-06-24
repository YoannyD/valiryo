# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api, _
from collections import defaultdict
from odoo.tools import float_is_zero
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    required_vat = fields.Boolean("Vat requerido", default=False)
    

class AccountMove(models.Model):
    _inherit = "account.move"
    
    transferencia_bancaria = fields.Boolean("Transferencia bancaria")
    payment_mode_id = fields.Many2one('account.payment.mode', string='Modo de pago',
                                      domain=[('payment_type', '=', 'outbound')])
    
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

        if self.partner_id.payment_mode_id:
            self.payment_mode_id = self.partner_id.payment_mode_id
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

    def _get_invoiced_lot_values(self):
        """ Get and prepare data to show a table of invoiced lot on the invoice's report. """
        self.ensure_one()

        res = super(AccountMove, self)._get_invoiced_lot_values()

        sale_lines = self.invoice_line_ids.sale_line_ids
        sale_orders = sale_lines.order_id
        stock_move_lines = sale_lines.move_ids.filtered(lambda r: r.state == 'done').move_line_ids

        # Get the other customer invoices and refunds.
        ordered_invoice_ids = sale_orders.mapped('invoice_ids')\
            .filtered(lambda i: i.state not in ['draft', 'cancel'])\
            .sorted(lambda i: (i.invoice_date, i.id))

        # Get the position of self in other customer invoices and refunds.
        self_index = None
        i = 0
        for invoice in ordered_invoice_ids:
            if invoice.id == self.id:
                self_index = i
                break
            i += 1

        # Get the previous invoices if any.
        previous_invoices = ordered_invoice_ids[:self_index]

        # Get the incoming and outgoing sml between self.invoice_date and the previous invoice (if any) of the related product.
        write_dates = [wd for wd in self.invoice_line_ids.mapped('write_date') if wd]
        self_datetime = max(write_dates) if write_dates else None
        last_invoice_datetime = dict()
        for product in self.invoice_line_ids.product_id:
            last_invoice = previous_invoices.filtered(lambda inv: product in inv.invoice_line_ids.product_id)
            last_invoice = last_invoice[-1] if len(last_invoice) else None
            last_write_dates = last_invoice and [wd for wd in last_invoice.invoice_line_ids.mapped('write_date') if wd]
            last_invoice_datetime[product] = max(last_write_dates) if last_write_dates else None

        def _filter_incoming_sml(ml):
            if ml.state == 'done' and ml.location_id.usage == 'customer' and ml.lot_id:
                last_date = last_invoice_datetime.get(ml.product_id)
                if last_date:
                    return last_date <= ml.date <= self_datetime
                else:
                    return ml.date <= self_datetime
            return False

        def _filter_outgoing_sml(ml):
            if ml.state == 'done' and ml.location_dest_id.usage == 'customer' and ml.lot_id:
                last_date = last_invoice_datetime.get(ml.product_id)
                if last_date:
                    return last_date <= ml.date <= self_datetime
                else:
                    return ml.date <= self_datetime
            return False

        incoming_sml = stock_move_lines.filtered(_filter_incoming_sml)
        outgoing_sml = stock_move_lines.filtered(_filter_outgoing_sml)

        # Prepare and return lot_values
        qties_per_lot = defaultdict(lambda: 0)
        if self.move_type == 'out_refund':
            for ml in outgoing_sml:
                qties_per_lot[ml.lot_id] -= ml.product_uom_id._compute_quantity(ml.qty_done, ml.product_id.uom_id)
            for ml in incoming_sml:
                qties_per_lot[ml.lot_id] += ml.product_uom_id._compute_quantity(ml.qty_done, ml.product_id.uom_id)
        else:
            for ml in outgoing_sml:
                qties_per_lot[ml.lot_id] += ml.product_uom_id._compute_quantity(ml.qty_done, ml.product_id.uom_id)
            for ml in incoming_sml:
                qties_per_lot[ml.lot_id] -= ml.product_uom_id._compute_quantity(ml.qty_done, ml.product_id.uom_id)
        lot_values = res
        for lot_id, qty in qties_per_lot.items():
            if float_is_zero(qty, precision_rounding=lot_id.product_id.uom_id.rounding):
                continue
            lot_values.append({
                'product_name': lot_id.product_id.display_name,
                'quantity': self.env['ir.qweb.field.float'].value_to_html(qty, {'precision': self.env['decimal.precision'].precision_get('Product Unit of Measure')}),
                'uom_name': lot_id.product_uom_id.name,
                'lot_name': lot_id.name,
                # The lot id is needed by localizations to inherit the method and add custom fields on the invoice's report.
                'lot_id': lot_id.id
            })
        return lot_values
