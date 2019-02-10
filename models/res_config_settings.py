# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime

from werkzeug import urls

from odoo import api, fields, models, tools



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    point = fields.Integer(related='company_id.point', string="Point", readonly=False)
    module_account_accountant = fields.Boolean(string='Account Accountant')
    module_l10n_fr_hr_payroll = fields.Boolean(string='French Payroll')
    module_l10n_be_hr_payroll = fields.Boolean(string='Belgium Payroll')
    module_l10n_in_hr_payroll = fields.Boolean(string='Indian Payroll')

