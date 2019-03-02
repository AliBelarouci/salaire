from odoo import models, fields, api, _
# from datetime import date, datetime, time
# from dateutil.relativedelta import relativedelta
# from odoo.exceptions import ValidationError

class DACWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.dac.report.wizard"
    _description = "Wizard For DAC Report"
    # period = fields.Char(string="Périod", required=True, )

    # dec_cnas =fields.Char(string="Date Affiliation", related="res.company.dec_cnas" )

