from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class CasePendingInformation(models.Model):
    _name = 'case.pending.info'
    _description = 'Case Pending Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'court_name'

    land_case_id = fields.Many2one('land.info', string='Land Area', required=True, ondelete='cascade')

    court_name = fields.Char(string='Court Name', tracking=True)
    case_no = fields.Char(string='Case No', tracking=True)
    case_stage = fields.Char(string='Case Stage')
    case_next_date = fields.Date(string='Case Next DATE', tracking=True)
    judgement = fields.Text(string='Judgement')

    CASE_STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('hearing', 'Under Hearing'),
        ('investigation', 'Investigation'),
        ('judgment', 'Judgment'),
        ('closed', 'Closed')
    ]

    name = fields.Char(string="Case Reference", required=True, readonly=True, default="New")

    case_status = fields.Selection(
        CASE_STATUS,
        string="Case Status",
        default='draft',
        tracking=True
    )

    # ✅ Buttons for status change
    def action_set_pending(self):
        self.case_status = 'pending'

    def action_set_hearing(self):
        self.case_status = 'hearing'

    def action_set_investigation(self):
        self.case_status = 'investigation'

    def action_set_judgment(self):
        self.case_status = 'judgment'

    def action_set_closed(self):
        self.case_status = 'closed'

    def action_set_draft(self):
        for rec in self:
            rec.case_status = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('case.pending.info') or '00001'
            vals['name'] = f"CPI/{year}/{month_name}/{seq}"
        return super(CasePendingInformation, self).create(vals)
