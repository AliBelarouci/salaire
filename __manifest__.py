# -*- coding: utf-8 -*-
{
    'name': "salaire",
    'sequence':'1',

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [

        'hr_contract',
        'hr_holidays',
        'decimal_precision',
    ],

    # always loaded
    'data': [

         'data/hr_payroll_categories.xml',
         'data/hr_payroll_data100.xml',
         'data/hr_payroll_data200.xml',
         'data/hr_payroll_data300.xml',
         'data/hr_payroll_data.xml',
         'data/A4_paper.xml',
         'data/crons.xml',
         'data/ats_paper.xml',
         'security/user_groups.xml',
         'security/rules.xml',
         'security/ir.model.access.csv',


         'wizard/menu.xml',
         'wizard/salaire_ats_wizard.xml',
         'wizard/divers/attestation/views.xml',
         'wizard/CNAS/EMS.xml',


         'report/ats_page1_report_view.xml',
         'report/ats_page2_report_view.xml',
         'report/attestation.xml',
         'report/report_payslip.xml',
         'report/report_menu.xml',
         'views/hr_contract_views.xml',
         'views/hr_employee_views.xml',

        #'views/res_config_settings_views.xml',
         'views/hr_payslip_views.xml',

        'views/views.xml',
        'views/templates.xml',
        'views/report_payslip_templates.xml',
        'views/class-categ.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
'installable': True,
    'application': True
}