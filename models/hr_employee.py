# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    #slip_ids = fields.One2many('hr.payslip', 'employee_id', string='Payslips', readonly=True)
    #payslip_count = fields.Integer(compute='_compute_payslip_count', string='Payslip Count', groups="hr_payroll.group_hr_payroll_user")
    prenom = fields.Char(string="Prenom", required=True, )
    numSS = fields.Char(string="Num Sécurité Sociale", required=True, )


    @api.multi
    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = len(employee.slip_ids)

    @api.model
    def get_contract(self, employee, date_from, date_to,type=0):
        """
        @param employee: recordset of employee
        @param date_from: date field
        @param date_to: date field
        @return: returns the ids of all the contracts for the given employee that need to be considered for the given dates
        """
        # a contract is valid if it ends between the given dates
        clause_1 = ['&', ('date_end', '<=', date_to), ('date_end', '>=', date_from)]
        # OR if it starts between the given dates
        clause_2 = ['&', ('date_start', '<=', date_to), ('date_start', '>=', date_from)]
        # OR if it starts before the date_from and finish after the date_end (or never finish)
        clause_3 = ['&', ('date_start', '<=', date_from), '|', ('date_end', '=', False), ('date_end', '>=', date_to)]
        close=[('state', '=', 'close')]
        open=[('state', '=', 'open')]
        draft=[('state', '!=', 'draft')]
        clause_final = [('employee_id', '=', employee.id)]
        if type==0:
            clause_final=clause_final+open
        if type==1:
            clause_final = clause_final + close
        if type==2:
            clause_final = clause_final + draft

        clause_final = clause_final+[ '|'] + clause_1 + clause_2

        return self.env['hr.contract'].search(clause_final).ids
