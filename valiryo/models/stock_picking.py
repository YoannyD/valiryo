# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"
    
    sale_country_id = fields.Char(related="sale_id.sale_country_id.name", store=True)
    marketplace = fields.Boolean(related="sale_id.marketplace", store=True)