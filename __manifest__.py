{
    'name':'HMS',
    'version':'1.0',
    'category':'Hospital',
    'depends': ['base','crm'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/hms_rules.xml', 
        'views/patient_views.xml',
        'views/department_view.xml',
        'views/doctor_view.xml',
        "views/res_partner_views.xml",
        'report/patient_report.xml',
        'report/report_patient_status.xml',
    ],
    'installable': True,
    
}
