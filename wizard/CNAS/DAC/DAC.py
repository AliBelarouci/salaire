from odoo import models, fields, api, _
# from datetime import date, datetime, time
# from dateutil.relativedelta import relativedelta
# from odoo.exceptions import ValidationError
class DACWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.dac.report.wizard"
    _description = "Wizard For DAC Report"
    # period = fields.Char(string="Périod", required=True, )
    def _compute_selection(self):
        active_model = self._name
        # dec_cnas
        if self.env.user.company_id.read()[0]['dec_cnas'] == "mens":
            period = [
                      ('1', 'Janvier'),
                      ('2', 'Février'),
                      ('3', 'Mars'),
                      ('4', 'Avril'),
                      ('5', 'Mai'),
                      ('6', 'Juin'),
                      ('7', 'Juillet'),
                      ('8', 'Août'),
                      ('9', 'Septembre'),
                      ('10', 'Octobre'),
                      ('11', 'Novembre'),
                      ('12', 'Décembre'),
                      ]
        else:
            period = [
                ('T1', 'Trimestre 1'),
                ('T2', 'Trimestre 2'),
                ('T3', 'Trimestre 3'),
                ('T4', 'Trimestre 4'),
            ]
        return period
    period = fields.Selection(selection=lambda self: self._compute_selection(), string="Period",)
    select_period = fields.Char(string="Period Selectionne", compute="_period_s")
    year_fiscal = fields.Integer(string="Year Fiscal", compute="_get_yearFiscal")

    def _get_yearFiscal(self):
        self.year_fiscal = 2019
        # self.env['year_fisc'].getActive()
    @api.depends('period')
    def _period_s(self):
        self.select_period = self.period

