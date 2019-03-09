from odoo import models, fields, api, _

from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
# from odoo.exceptions import ValidationError
class DACWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.dac.report.wizard"
    _description = "Wizard For DAC Report"
    # period = fields.Char(string="Périod", required=True, )
    date_start = fields.Date(string ='Date Start', required=True)
    date_end = fields.Date(string   ='Date End', required=True)
    ASSIETTE = fields.Float(string="ASSIETTE",  readonly=True )
    detail_ids = fields.One2many(comodel_name="salaire.dac.report.wizard.detail", inverse_name='dac_id')
    mouvement_ids = fields.One2many(comodel_name="salaire.dac.report.wizard.mouvement", inverse_name='dac_id',string='Mouvement')
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
            # self.ASSIETTE =self.getASSIETTE()


    # select_period = fields.Char(string="Period Selectionne", compute="_period_s")
    year_fiscal = fields.Integer(string="Year Fiscal", default=lambda self: self._get_yearFiscal())
    state = fields.Selection([
        ('draft', 'New'),
        ('done', 'Done'),
        ('error', 'Error'),

    ], string='Status',
        track_visibility='onchange', help='Status of the ATS', default='draft')

    def _get_yearFiscal(self):
        return self.env['year_fisc'].getActive()
        #
    def getASSIETTE(self):
        clause_1 = ['&', ('date_from', '>=', self.date_start), ('date_from', '<=', self.date_end)]
        clause_final = [('state', '=', 'done')] + clause_1
        payslip_ids = self.env['hr.payslip'].search(clause_final).read()
        TotG = 0
        result_dict = {}
        for payslip in payslip_ids:
            clause_1 = [('code', '=', 'GROSS')]
            _clause1 = [('slip_id', '=', payslip['id']), ('code', '=', 'GROSS')]
            _clause2 = [('slip_id', '=', payslip['id']), ('code', '=', 'RSS')]
            sorted_rules1 = self.env['hr.payslip.line'].browse(payslip['line_ids']).search(_clause1).read()
            TotG =TotG+ sorted_rules1[0]['amount']
            result_dict[payslip['id']] = {
                'py_name': payslip['name'],
                'empolyee_id': payslip['employee_id'][0],
                'TotG': sorted_rules1[0]['amount'],
            }
        lines = [(0, 0, line) for line in list(result_dict.values())]
        for ats in self:
            ats.detail_ids.unlink()
            ats.write({'detail_ids': lines})
        employee_ids = self.env['hr.employee'].search([])
        mouvement_dict = {}
        for employee in employee_ids:
            contract_ids= self.get_contract2(employee,self.date_start,self.date_end)
            if  contract_ids != False:
                contract=self.env['hr.contract'].browse(contract_ids['contract_ids']).read()[0]
                mouvement_dict[employee.id] = {
                    'empolyee_id': employee.id,
                    'mouvement': contract_ids['mouvement'],
                    'date_start': contract['date_start'],
                    'date_end': contract['date_end'],
                    'name': contract['name'],

                }
        mouvement_lines = [(0, 0, line) for line in list(mouvement_dict.values())]
        for ats in self:
            ats.mouvement_ids.unlink()
            ats.write({'mouvement_ids': mouvement_lines})



        self.ASSIETTE = TotG
        return TotG

    @api.model
    def get_contract2(self, employee, date_from, date_to):
        """
        @param employee: recordset of employee
        @param date_from: date field
        @param date_to: date field
        @param type: 0 for new contract 1 for end contract 2 for valid contract
        @return: returns the ids of all the contracts for the given employee that need to be considered for the given dates
        """
        # a contract is valid if it ends between the given dates
        clause_0 = ['&', ('date_end', '<=', date_to), ('date_end', '>=', date_from)]
        # OR if it starts between the given dates
        clause_1 = ['&', ('date_start', '<=', date_to), ('date_start', '>=', date_from)]
        # OR if it starts before the date_from and finish after the date_end (or never finish)
        clause_2 = ['&', ('date_start', '<=', date_from), '|', ('date_end', '=', False), ('date_end', '>=', date_to)]

        clause_final = [('employee_id', '=', employee.id)]

        contract_ids= self.env['hr.contract'].search(clause_final + clause_0).ids
        if len(contract_ids) > 0:
            return {'contract_ids':contract_ids,'mouvement':'END'}
        contract_ids = self.env['hr.contract'].search(clause_final + clause_1).ids
        if len(contract_ids) > 0:
            return {'contract_ids': contract_ids, 'mouvement': 'NEW'}
        contract_ids = self.env['hr.contract'].search(clause_final + clause_2).ids
        if len(contract_ids) > 0:
            return {'contract_ids': contract_ids, 'mouvement': 'VALID'}
        return False

class DAC_detail(models.TransientModel):
    _name = 'salaire.dac.report.wizard.detail'
    py_name = fields.Char(string="Ref", required=False, )
    empolyee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False, )
    TotG  = fields.Integer(string="Totale Gain", required=False, )
    dac_id = fields.Many2one(comodel_name='salaire.dac.report.wizard', string='DAC', ondelete="cascade")
class DAC_mouvement(models.TransientModel):
    _name = 'salaire.dac.report.wizard.mouvement'
    empolyee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False, )
    mouvement = fields.Char()
    name = fields.Char('Contract Reference',)
    date_start = fields.Date('Start Date',
                             help="Start date of the contract.")
    date_end = fields.Date('End Date',
                           help="End date of the contract (if it's a fixed-term contract).")

    dac_id = fields.Many2one(comodel_name='salaire.dac.report.wizard', string='DAC', ondelete="cascade")



