from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import re

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient Record'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    age = fields.Integer(compute="_compute_age", store=True)
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a+', 'A+'), ('b+', 'B+'), ('o+', 'O+'),
    ], string='Blood Type')
    pcr = fields.Boolean()
    image = fields.Binary(attachment=True)
    address = fields.Text()
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    def action_set_undetermined(self):
        self.state = 'undetermined'

    def action_set_good(self):
        self.state = 'good'

    def action_set_fair(self):
        self.state = 'fair'

    def action_set_serious(self):
        self.state = 'serious'


    doctors_ids = fields.Many2many("hms.doctors", string="Doctors")
    log_ids = fields.One2many('hms.log', 'patient_id')
    department_id = fields.Many2one('hms.department', string="Department")
    department_capacity = fields.Integer(related='department_id.capacity', readonly=True)

    related_partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        ondelete='cascade',
    )
    @api.model
    def create(self, vals):
        vals.setdefault('related_partner_id', self.env.user.partner_id.id)
        return super().create(vals)


    @api.depends("birth_date")
    def _compute_age(self):
        today = date.today()
        for rec in self:
            rec.age = (today - rec.birth_date).days // 365 if rec.birth_date else 0

    email = fields.Char(string="Email", index=True, required=True)

    _sql_constraints = [
        ("patient_email_unique", "UNIQUE(email)", "e‑mail must be unique"),
    ]

    @api.constrains("email")
    def _check_email_format(self):
        for rec in self:
            if rec.email and not EMAIL_REGEX.match(rec.email):
                raise ValidationError("Invalid e‑mail format!")


    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Checked",
                    'message': "PCR field has been automatically checked because age is less than 30."
                }
            }

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required")



    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if vals.get('state'):
            self.env['hms.log'].create({
                'patient_id': rec.id,
                'description': f"{vals['state']}"
            })
        return rec

    def write(self, vals):
        for rec in self:
            old_state = rec.state
            res = super(Patient, rec).write(vals)
            if 'state' in vals and vals['state'] != old_state:
                self.env['hms.log'].create({
                    'patient_id': rec.id,
                    'description': f"{vals['state']}"
                })
        return res



