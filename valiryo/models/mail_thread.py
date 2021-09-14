# -*- coding: utf-8 -*-
# © 2021 Voodoo - <hola@voodoo.es>

import re
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
    
    @api.model
    def create(self, vals):
        context = dict(self.env.context)
        auto_add_follower = self.env['ir.config_parameter'].sudo().get_param('auto_add_followers', default=False)
        if "add_follower" not in self.env.context and not auto_add_follower:
            context.update({
                "mail_create_nosubscribe": True,
                "add_follower": False
            })
        else:
            context.update({"add_follower": True})

        self = self.with_context(context)
        return super(MailThread, self).create(vals)