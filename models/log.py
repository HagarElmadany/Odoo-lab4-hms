from odoo import models, fields, api

class Log(models.Model):
    _name = 'hms.log'
    _description = 'Patient Log History'

    patient_id = fields.Many2one('hms.patient')
    description = fields.Text()
    created_by = fields.Many2one('hms.doctors', string="Created By")
    date = fields.Datetime(default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        if not vals.get('created_by'):
            vals['created_by'] = 1  
        return super().create(vals)
