from odoo import models, fields, api, _
# from datetime import date, datetime, time
# from dateutil.relativedelta import relativedelta
# from odoo.exceptions import ValidationError

class EMSWizard(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "salaire.ems.report.wizard"
    _description = "Wizard For ATS Report"
    # period = fields.Char(string="Périod", required=True, )
    date_start = fields.Date('Start Date', required=True, default=fields.Date.today,
                             help="Start date of the contract.")
    date_end = fields.Date('End Date',
                           help="End date of the contract (if it's a fixed-term contract).")
    employee_ids = fields.One2many(comodel_name="salaire.ems.employees", inverse_name="ems_id", string="Employees", required=False, )
    # employee_ids = fields.Many2many('hr.employee', string= 'Employees')
    # employee_ids = fields.One2many(comodel_name="hr.employee", inverse_name="", string="", required=False, )

    def charge_employees(self):
        result_dict = {}
        employee_ids = self.env['hr.employee'].search([])
        for employee in employee_ids:
            contract_ids= self.env['hr.employee'].get_contract(employee,self.date_start,self.date_end,2)
            contracts= self.env['hr.contract'].browse(contract_ids)
            if len(contracts)>0:
                # .strftime('%m/%d/%Y')
                # .strftime('%m/%d/%Y')
                E_S = 'S'
                date_E_S = contracts[0].date_end if contracts[0].state == 'close' else contracts[0].date_start
                E_S = 'S' if contracts[0].state == 'close' else 'E'
                result_dict[employee.id] = {
                    'numss': employee.numSS,
                    'np': employee.name,
                    'birthday': employee.birthday,
                    'E_S': E_S,
                    'date_E_S': date_E_S,
                }


        lines = [(0, 0, result_dict[line]) for line in sorted(result_dict.keys())]
        # lines = [(0, 0, line) for line in list(result_dict.values())]
        for EMS in self:
            EMS.employee_ids.unlink()
            EMS.write({'employee_ids': lines})
        return
class EMSEmployeeList(models.TransientModel):
    _name = "salaire.ems.employees"
    ems_id = fields.Many2one(comodel_name='salaire.ems.report.wizard', string='EMS', ondelete="cascade")
    numss = fields.Char("Num SECURITE SOCIALE")
    np = fields.Char("NOM ET PRENOM")
    birthday= fields.Date(string='DATE DE NAISSANCE',  )
    E_S = fields.Char("E/S")
    date_E_S = fields.Date(string='DATE ENTREE/SORTIE',   )
    obs = fields.Char("OBSERVATION")


