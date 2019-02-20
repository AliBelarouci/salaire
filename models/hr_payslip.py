

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
import calendar

from dateutil.relativedelta import relativedelta
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    line_ids = fields.One2many('hr.payslip.line', 'slip_id', string='Payslip Lines', readonly=True,
                               ondelete='cascade',
                               states={'draft': [('readonly', False)]})
    date_to = fields.Date(string='Date To', readonly=True, required=True,
                          default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),
                           )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft',
        help="""* When the payslip is created the status is \'Draft\'
                \n* If the payslip is under verification, the status is \'Waiting\'.
                \n* If the payslip is confirmed then status is set to \'Done\'.
                \n* When user cancel payslip the status is \'Rejected\'.""")
    @api.onchange('date_from', 'date_to')
    def onchange_date(self):
        date_from = datetime.strftime(self.date_from,'%d/%m/%Y')
        return
        c=calendar.monthrange(self.date_to.year,self.date_to.month)
        if self.date_from.day != 1:
            raise ValidationError(_('Error! from start incorrect.'))
        if not self.date_to.day == c[1] or not (self.date_to.year==self.date_from.year) or not (self.date_to.month == self.date_from.month) :
            raise ValidationError(_('Error! to start incorrect.'))




    @api.multi
    def unlink(self):
        if any(self.filtered(lambda payslip: payslip.state not in ('draft', 'cancel'))):
            raise UserError(_('You cannot delete a payslip which is not draft or cancelled!'))
        for line in self.line_ids:
            line.unlink()
        return super(HrPayslip, self).unlink()

    # @api.multi
    # def to_cancel(self):
    #     return self.write({'state': 'draft'})
    @api.multi
    def to_cancel(self):
        if self.filtered(lambda slip: slip.state == 'done'):
            raise UserError(_("Cannot cancel a payslip that is done."))
        return self.write({'state': 'cancel'})
    @api.multi
    def action_payslip_cancel1(self):
        if self.filtered(lambda slip: slip.state == 'done11'):
            raise UserError(_("Cannot cancel a payslip that is done.222"))
        return self.write({'state': 'cancel'})

    @api.multi
    def action_payslip_cancel(self):
        if self.filtered(lambda slip: slip.state == 'done'):
            raise UserError(_("Cannot cancel a payslip that is done."))
        return self.write({'state': 'cancel'})
    @api.multi
    def print_sheet(self):
        report = self.env.ref('salaire.action_report_payslip')
        return report.report_action(self)

    def process_demo_scheduler_queue(self, context=None):
        raise UserError(_("the cron is runing."))

    def compute_IRG(self,Tranche):
        IRG = 0
        if Tranche > 0 and Tranche <=10000:
            IRG = 0
        if Tranche > 10000 and Tranche <=30000:
            IRG = (Tranche-10000)*0.2
        if Tranche > 30000 and Tranche <=120000:
            IRG = ((Tranche-30000)*0.3)+4000
        return IRG
    def compute_Abatt(self,IRGBRUT):
        abatt = IRGBRUT*0.4
        if abatt < 1000:
            return 1000
        if abatt > 1500:
            return 1500
        return abatt



