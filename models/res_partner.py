from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
        ondelete='restrict'
    )

    @api.constrains('email')
    def _check_email_unique_in_patients(self):
        for partner in self:
            if partner.email:
                patient = self.env['hms.patient'].search([('email', '=', partner.email)], limit=1)
                if patient:
                    raise ValidationError("This email already exists in patient records.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You cannot delete a customer linked to a patient.")
        return super().unlink()
