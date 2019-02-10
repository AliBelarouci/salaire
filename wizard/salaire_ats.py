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
    def compute_ats(self):
        date_end = self.date_start - relativedelta(months=self.months_nbr-1)
        clause_1 = ['&', ('date_from', '<=', self.date_start), ('date_to', '>=', date_end)]
        clause_final = [('employee_id', '=', self.employee_id.id) , '&' , ('state', '=', 'done')] + clause_1

        self.payslip_ids = self.env['hr.payslip'].search(clause_final)
        return []
class ATSWizardLines(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.ats.report.wizard.lines"
    _description = "Wizard For ATS Report"

    month = fields.Char('Month')
    jourTrav = fields.Integer('Jours Trav')
    TotG = fields.Float("Totale Gaine")
    RSS = fields.Float('RSS')
    ats_id = fields.Many2one(comodel_name='salaire.ats.report.wizard', string='ATS ', ondelete="cascade")












