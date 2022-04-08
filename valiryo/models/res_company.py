# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = 'res.company'

    custom_invoice = fields.Boolean('Reporte personalizado de factura', default=False)
    


