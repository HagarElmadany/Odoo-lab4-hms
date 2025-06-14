from odoo import models

class PatientReport(models.AbstractModel):
    _name = 'report.hms.report_patient_status'
    _description = 'Patient Status Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['hms.patient'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hms.patient',
            'docs': docs,
        }
