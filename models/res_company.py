from odoo import api, fields, models
class ResCompny(models.Model):
    _inherit = 'res.company'
    # active = fields.Boolean(string="Active")
    numSS = fields.Char(string="Num Sécurité Sociale", required=True, )
    nom = fields.Char(string="Raison sociale", required=True, )
    gerant = fields.Char(string="Gerant", required=True, )

    dateAff = fields.Char(string="Date Affiliation", required=True, )
    raison = fields.Selection([
        ('raison1', 'raison1'),
        ('raison2', 'raison2'),
    ], string='Raison sociale', default='raison1')
    caisseCnas = fields.Selection([
        ('cnas39', 'Agence Cnas Eloued'),
        ('cnas30', 'Agence Cnas Ouargla'),
    ], string='Caisse Cnas', default='cnas39')
    centre = fields.Selection([
        ('ctr39', 'Eloued'),
        ('ctr30', 'Ouargla'),
    ], string='Centre', default='ctr39')
    dec_cnas = fields.Selection([
        ('mens', 'Mensuelle'),
        ('tri', 'Trimestrielle'),

    ], string='Declaration Cnas', default='tri')
    dec_g29 = fields.Selection([
        ('tri', 'Trimestrielle'),
    ], string='Declaration G29', default='tri')
    def print_method(self):
        print(self)
    def Active_company(self):
        for c in self:
            id=c.read()[0]['id']
            context = self._context
            current_uid = context.get('uid')
            user = self.env['res.users'].sudo().browse(current_uid).write({'company_id': id})




