from odoo import models, fields, api, _
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class ATTWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.att.report.wizard"
    _description = "Wizard For Attestation Report"
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,)
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True,)

    @api.multi
    def print_att(self):
        if not self.employee_id or not self.contract_id :
            raise ValidationError(_('Error! date start incorrect.'))
            return

        report = self.env.ref(
            'salaire.salaire_report_att')
        return report.report_action(self)

