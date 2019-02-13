from odoo import api, fields, models


class ResCompny(models.Model):
    _inherit = 'res.company'
    _description = 'Employee'

    numSS = fields.Char(string="Num Sécurité Sociale", required=True, )
    # nom = fields.Char(string="Raison sociale", required=True, )
    gerant = fields.Char(string="Gerant", required=True, )
    dateAff = fields.Char(string="Date Affiliation", required=True, )
    caisseCnas = fields.Selection([
        ('cnas39', 'Agence Cnas Eloued'),
        ('cnas30', 'Agence Cnas Ouargla'),
    ], string='Caisse Cnas', default='cnas39')
    centre = fields.Selection([
        ('ctr39', 'Eloued'),
        ('ctr30', 'Ouargla'),
    ], string='Centre', default='ctr39')
    dec_cnas = fields.Selection([
        ('tri', 'Trimestrielle'),

    ], string='Declaration Cnas', default='tri')
    dec_g29 = fields.Selection([
        ('tri', 'Trimestrielle'),
    ], string='Declaration G29', default='tri')

