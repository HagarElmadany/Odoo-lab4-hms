from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctors'
    _description = 'Doctors'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Binary(attachment=True)
    patient_ids = fields.Many2many('hms.patient')

