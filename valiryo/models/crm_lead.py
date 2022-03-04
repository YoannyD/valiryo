# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class crm_lead(models.Model):
    _inherit = "crm.lead"
    
    categoria_cliente = fields.Many2many('res.partner.category',related='res_partner_category_id', store=True)
    realizado = fields.Boolean("Realizado")
