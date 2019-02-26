from odoo import models, fields, api, _
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class ATTESTATIONWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.attestation.report.wizard"
    _description = "Attestation de Travaille"
    employee_id = fields.Many2one('hr.employee', 'Employee')