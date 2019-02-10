# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ResCompany(models.Model):
    _inherit = 'res.company'

    point = fields.Integer(string='Point')

class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.contract'
    _description = 'Employee Contract'
    #name = fields.Char(compute="new_name",required=False)
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')
    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),
    ], string='Scheduled Pay', index=True, default='monthly',
    help="Defines the frequency of the wage payment.")
    resource_calendar_id = fields.Many2one(required=True, help="Employee's working schedule.")
    class_id = fields.Many2one(comodel_name='hr.class', string='Classe')
    categ_id = fields.Many2one(comodel_name='hr.categ', string='Categ')
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('close', 'Expired'),


    ], string='Status', group_expand='_expand_states',
       track_visibility='onchange', help='Status of the contract', default='draft')

    @api.model
    def create(self, vals):
        contract_ids = self.search([('employee_id', '=', vals.get('employee_id')), ('state', '=', 'open')])
        if len(contract_ids)!=0:
            raise ValidationError(_('Error! You must close all other contract berfor insert a new.'))
        else:

            Contract = super(HrContract, self).create(vals)
            return Contract
    # @api.multi
    # @api.onchange('date_start')
    # def _onchange_date_start(self):
    #     #('employee_id', '=', self.employee_id.id), '&',
    #     #self.ensure_one()
    #
    #     clause = [('id', '!=', self), ('employee_id', '=', self.employee_id.id), ( 'date_end', '>', fields.Date.to_string(self.date_start))]
    #     clause1 = [('employee_id', '=', self.employee_id.id)]
    #     contract_ids = self.env['hr.contract'].search(clause1).ids
    #     if len(contract_ids) != 0:
    #         raise ValidationError(_('Error! date start incorrect.'))
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id
            self.department_id = self.employee_id.department_id
            self.resource_calendar_id = self.employee_id.resource_calendar_id
        clause = [('employee_id', '=', self.employee_id.id),  ('state', '=', 'open')]
        contract_ids = self.env['hr.contract'].search(clause).ids
        if len(contract_ids) != 0:
            raise ValidationError(_('00 Error! You must close all other contract berfor insert a new.'))

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'close':
            if not self.date_end:
                raise ValidationError(_('Error! You must set the close date'))
        # if self.state == 'open' or self.state == 'druft' :
        #     clause = [(self.date_start, '>', 'date_end')]




class HrClass(models.Model):
    _name = 'hr.class'
    _rec_name = 'cls'
    cls = fields.Integer('Classe')
    index_cls = fields.Integer('Index')
    categ_ids = fields.One2many(comodel_name="hr.categ",inverse_name='class_id')
    sequence = fields.Integer('sequence')

class hrCateg(models.Model):
    _name = 'hr.categ'
    _rec_name = 'categ'
    categ = fields.Integer('Categ')
    index_iep = fields.Integer('Index IEP')
    class_id = fields.Many2one(comodel_name='hr.class',string='Classe', ondelete="cascade")
    sequence = fields.Integer('sequence')
class HrContractAdvandageTemplate(models.Model):
    _name = 'hr.contract.advantage.template'
    _description = "Employee's Advantage on Contract"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    lower_bound = fields.Float('Lower Bound', help="Lower bound authorized by the employer for this advantage")
    upper_bound = fields.Float('Upper Bound', help="Upper bound authorized by the employer for this advantage")
    default_value = fields.Float('Default value for this advantage')
