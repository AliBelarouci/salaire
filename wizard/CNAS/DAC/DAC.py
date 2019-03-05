from odoo import models, fields, api, _

from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
# from odoo.exceptions import ValidationError
class DACWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.dac.report.wizard"
    _description = "Wizard For DAC Report"
    # period = fields.Char(string="Périod", required=True, )
    date_start = fields.Date(string ='Date Start', required=True,)
    date_end = fields.Date(string   ='Date End', required=True,)


    # default=lambda self: fields.Date.to_string(date.today().replace(day=1))
    def _compute_selection(self):
        active_model = self._name
        #
        # cc=self.env['res.company'].search(['id','=','1'])
        dec_cnas= 'mens'
        # self.env.user.company_id.read()[0]['dec_cnas']
        if   dec_cnas=='tri':
            period = [
                      (1, 'Janvier'),
                      (2, 'Février'),
                      (3, 'Mars'),
                      (4, 'Avril'),
                      (5, 'Mai'),
                      (6, 'Juin'),
                      (7, 'Juillet'),
                      (8, 'Août'),
                      (9, 'Septembre'),
                      (10, 'Octobre'),
                      (11, 'Novembre'),
                      (12, 'Décembre'),
                      ]

        else:
            period = [
                (1, 'Trimestre 1'),
                (2, 'Trimestre 2'),
                (3, 'Trimestre 3'),
                (4, 'Trimestre 4'),
            ]
        return period
    def default_period(self):
        if self.env.user.company_id.read()[0]['dec_cnas'] == "mens":
            return datetime.now().month
        else:
            return (datetime.now().month//3)


    period = fields.Selection(selection =lambda self: self._compute_selection(),
                              default=lambda self: self.default_period(), string="Period")
    @api.onchange('period')
    def onchange_period(self):
        if self.period:
            if self.env.user.company_id.read()[0]['dec_cnas'] == "mens":
                month=self.period
                date_start = date(self.env['year_fisc'].getActive(), month, 1)
                date_end = date_start + relativedelta(months=+1, day=1, days=-1)
                self.date_start = date_start
                self.date_end = date_end
            else:
                month = ((self.period*3)-3)+1
                date_start = date(self.env['year_fisc'].getActive(), month, 1)
                date_end = date_start + relativedelta(months=+3, day=1, days=-1)
                self.date_start = date_start
                self.date_end = date_end

    select_period = fields.Char(string="Period Selectionne", compute="_period_s")
    year_fiscal = fields.Integer(string="Year Fiscal", default=lambda self: self._get_yearFiscal())

    def _get_yearFiscal(self):
        return self.env['year_fisc'].getActive()
        #
    @api.depends('period')
    def _period_s(self):
        self.select_period = self.period

