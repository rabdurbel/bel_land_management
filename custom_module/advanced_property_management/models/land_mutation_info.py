from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class LandMutationInfo(models.Model):
    _name = 'land.mutation.info'
    _description = 'Land Mutation Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'land_mutation_id'
    # _order = 'last_tax_payment_date desc'

    name = fields.Char(string='Reference', readonly=True,
                       copy=False, default='New',
                       help='The reference code/sequence of the Land Mutation Info')
    land_mutation_id = fields.Many2one('land.info', string='Land Name', required=True, ondelete='cascade')
    owner_id = fields.Many2one('property.owner', string='Owner Name', tracking=True)
    khatian_no = fields.Char(string='Khatian No')
    dag_no = fields.Char(string='Dag No.')
    mutation_copy = fields.Binary(string='Mutation Copy', attachment=True)
    dcr_copy = fields.Binary(string='DCR Copy', attachment=True)

    #  5 STAGES
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Verification'),
        ('approve', 'Approved'),
        ('closed', 'Closed'),
    ], string="Status", default='draft', tracking=True)

    # 🔥 ACTION BUTTONS
    def action_verify(self):
        self.state = 'verify'

    def action_approve(self):
        self.state = 'approve'

    # def action_paid(self):
    #     self.state = 'paid'

    def action_cancel(self):
        for rec in self:
            if rec.state != 'closed':
                rec.state = 'closed'

    def action_reset_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('land.mutation.info') or '00001'
            vals['name'] = f"LMT/{year}/{month_name}/{seq}"
        return super(LandMutationInfo, self).create(vals)

    # @api.constrains('tax_payment_amount')
    # def _check_tax_amount(self):
    #     for record in self:
    #         if record.tax_payment_amount <= 0:
    #             raise ValidationError(_('Tax payment amount must be greater than zero!'))
