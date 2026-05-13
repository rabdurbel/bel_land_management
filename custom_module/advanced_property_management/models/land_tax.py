from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime



class LandTax(models.Model):
    _name = 'land.tax'
    _description = 'Land Tax Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'land_id'
    _order = 'last_tax_payment_date desc'


    name = fields.Char(string='Reference', readonly=True,
                       copy=False, default='New',
                       help='The reference code/sequence of the Land Tax')

    land_id = fields.Many2one('land.info', string='Land Name', required=True, ondelete='cascade')

    city_corporation_union = fields.Char(string='City Corporation Name')
    land_name = fields.Char(string='Land Name')
    total_land = fields.Float(string='Total Land (in decimal)')
    last_tax_payment_date = fields.Date(string='Last Tax Payment Date',  tracking=True)
    tax_payment_amount = fields.Float(string='Tax Payment Amount', tracking=True)
    mouza_name = fields.Char(string='Mouza Name')
    dag_no = fields.Char(string='Dag No.')

    LAND_TYPE = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('agricultural', 'Agricultural'),
    ]

    land_type = fields.Selection(LAND_TYPE, string='LAND TYPE')
    tax_payment_year = fields.Date(string='Tax Pyment Year', widget="date")
    payment_rashid_no = fields.Char(string='Payment Rashid No', tracking=True)
    attachment_rashid_copy = fields.Binary(string='Attachment Rashid Copy', attachment=True)

    active = fields.Boolean(string='Active', default=True)

    # ✅ 5 STAGES
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Verification'),
        ('approve', 'Approved'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], string="Status", default='draft', tracking=True)

    # 🔥 ACTION BUTTONS
    def action_verify(self):
        self.state = 'verify'

    def action_approve(self):
        self.state = 'approve'

    def action_paid(self):
        self.state = 'paid'

    def action_cancel(self):
        for rec in self:
            if rec.state != 'cancel':
                rec.state = 'cancel'

    def action_reset_draft(self):
        self.state = 'draft'




    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('land.tax') or '00001'
            vals['name'] = f"PLT/{year}/{month_name}/{seq}"
        return super(LandTax, self).create(vals)

    @api.constrains('tax_payment_amount')
    def _check_tax_amount(self):
        for record in self:
            if record.tax_payment_amount <= 0:
                raise ValidationError(_('Tax payment amount must be greater than zero!'))