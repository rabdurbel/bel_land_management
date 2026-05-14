from odoo import models, fields, api, _
from datetime import datetime


class BuildingStructure(models.Model):
    _name = 'building.structure'
    _description = 'Building Structure & Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'land_name'

    land_id = fields.Many2one('land.info', string='Land Reference', required=True)

    name = fields.Char(string='Reference', readonly=True,
                       copy=False, default='New',
                       help='The reference code/sequence of the property Building Structure')

    land_name = fields.Char(string='Land Name', related='land_id.land_name', store=True)
    khatian_no = fields.Selection(related='land_id.khatian_no', string='KHATIAN NO', store=True)
    mouza_name = fields.Many2one('mouza.name', string='Mouza Name', store=True)
    approval_date = fields.Date(string='Approved Date')
    plot_dag_no = fields.Char(string='Plot/Dag NO', related='land_id.plot_dag_no')

    structure_plan_approval_institute = fields.Char(string='Structure & Plan Approval Institute',tracking=True)
    attachment_copy = fields.Binary(string='Attachment Copy', attachment=True)


    active = fields.Boolean(string='Active', default=True)



    # ✅ STATE
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Verification'),
        ('approve', 'Approved'),
        ('done', 'Active'),
        ('cancel', 'Cancelled'),
    ], string="Status", default='draft', tracking=True)

    # 🔥 ACTION METHODS
    def action_verify(self):
        self.state = 'verify'

    def action_approve(self):
        self.state = 'approve'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_reset_draft(self):
        self.state = 'draft'




    @api.model_create_multi
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('building.structure') or '00001'
            vals['name'] = f"BSP/{year}/{month_name}/{seq}"
        return super(BuildingStructure, self).create(vals)