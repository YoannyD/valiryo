# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    bank_id = fields.Many2one("res.partner.bank", company_dependent=True, string="Cuenta bancaria")
    


