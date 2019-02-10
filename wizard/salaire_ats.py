from odoo import models, fields, api
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta


class ATSWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.ats.report.wizard"
    _description = "Wizard For ATS Report"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    date_start = fields.Date(string='Date From', readonly=True, required=True,
                             default=lambda self: fields.Date.to_string(date.today().replace(day=1))
                             )
    months_nbr = fields.Integer('Months Number')
    payslip_ids = fields.Many2many('hr.payslip', 'hr_payslip_group_rel', 'payslip_id', 'employee_id', 'Payslips')
    lines_ids = fields.One2many(comodel_name="salaire.ats.report.wizard.lines", inverse_name='ats_id')

    @api.multi
    def print_page1(self):
        data = {}
        data['employee_id'] = self.employee_id
        report = self.env.ref(
            'salaire.action_report_ats_page1')
        return report.report_action(self, data=data)

    def print_page2(self):
        data = {}
        data['employee_id'] = self.employee_id
        report = self.env.ref('salaire.action_report_ats_page2')
        return report.report_action(self, data=data)

    @api.multi
    def compute_ats(self):
        date_end = self.date_start - relativedelta(months=self.months_nbr - 1)
        clause_1 = ['&', ('date_from', '<=', self.date_start), ('date_to', '>=', date_end)]

        clause_final = [('employee_id', '=', self.employee_id.id), '&', ('state', '=', 'done')] + clause_1

        payslip_ids = self.env['hr.payslip'].search(clause_final).read()
        result_dict = {}
        for payslip in payslip_ids:
            clause_1 = [ ('code', '=', 'GROSS')]
            _clause1 = [('slip_id' ,'=' , payslip['id']),  ('code', '=', 'GROSS')]
            _clause2=[('slip_id', '=', payslip['id']),  ('code', '=', 'RSS')]
            sorted_rules1 = self.env['hr.payslip.line'].browse(payslip['line_ids']).search(_clause1).read()
            sorted_rules2 = self.env['hr.payslip.line'].browse(payslip['line_ids']).search(_clause2).read()
            TotG=sorted_rules1[0]['amount']
            RSS=sorted_rules2[0]['amount']
            year_month = datetime.strftime(payslip['date_from'], '%Y/%m')

            jourTrav=0
            result_dict[payslip['id']] ={

                'year_month':year_month,
                'jourTrav':jourTrav,
                'TotG':TotG,
                'RSS':RSS,

            }
        lines = [(0, 0, line) for line in list(result_dict.values())]
        for ats in self:
            ats.lines_ids.unlink()
            ats.write({'lines_ids': lines})


















        return []


class ATSWizardLines(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.ats.report.wizard.lines"
    _description = "Wizard For ATS Report"
    year_month = fields.Char('Year and Month')
    year = fields.Integer('Year')
    month = fields.Integer('Month')
    jourTrav = fields.Integer('Jours Trav')
    TotG = fields.Float("Totale Gaine")
    RSS = fields.Float('RSS')
    ats_id = fields.Many2one(comodel_name='salaire.ats.report.wizard', string='ATS ', ondelete="cascade")
