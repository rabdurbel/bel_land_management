from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class PropertyOwner(models.Model):
    _name = 'property.owner'
    _description = 'Property Owner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'current_owner'
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, readonly=True, default="New")

    field_name = fields.Char(string='Field Name', tracking=True)
    # current_owner = fields.Char(string='Current Owner', required=True, tracking=True)
    current_owner = fields.Many2one("res.partner",string='Current Owner', tracking=True)
    ownership_transfer_date = fields.Date(string='Ownership Transfer Date', tracking=True)
    deep_no_attachment = fields.Boolean(string='Deep No Attachment File', default=False)
    sub_register_office = fields.Char(string='Sub Register Office', tracking=True)
    current_owner_address = fields.Text(string='Current Owner Address')
    previous_owner_name = fields.Many2one("res.partner",string='Previous Owner Name',traking=True)
    previous_owner_address = fields.Text(string='Previous Owner Address')
    deep_regi_date = fields.Date(string='Deep Registration Date',tracking=True)
    description = fields.Text(string='Description')

    # Relations
    land_info_ids = fields.One2many('land.info', 'owner_id', string='Land Information')
    building_ids = fields.One2many('building.info', 'owner_id', string='Buildings')

    # Computed fields for stat buttons
    total_land_area = fields.Float(string='Total Land Area', compute='_compute_total_land_area', store=True)
    total_buildings = fields.Integer(string='Total Buildings', compute='_compute_total_buildings', store=True)

    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='draft', tracking=True)

    land_count = fields.Integer(
        string="Lands",
        compute="_compute_land_count",
        store=False
    )

    @api.model_create_multi
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('property.owner') or '00001'
            vals['name'] = f"PTO/{year}/{month_name}/{seq}"
        return super(PropertyOwner, self).create(vals)

    @api.depends('land_info_ids.total_land_area')
    def _compute_total_land_area(self):
        for record in self:
            record.total_land_area = sum(record.land_info_ids.mapped('total_land_area'))

    @api.depends('building_ids')
    def _compute_total_buildings(self):
        for record in self:
            record.total_buildings = len(record.building_ids)

    @api.constrains('ownership_transfer_date', 'deep_regi_date')
    def _check_dates(self):
        for record in self:
            if record.ownership_transfer_date and record.deep_regi_date:
                if record.deep_regi_date > record.ownership_transfer_date:
                    raise ValidationError(_('Deep registration date cannot be after ownership transfer date!'))

        # Count field


    # Compute
    def _compute_land_count(self):
        for rec in self:
            rec.land_count = self.env['land.info'].search_count([
                ('owner_id', '=', rec.id)
            ])

    # Smart button action
    def action_view_land(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Land Information',
            'res_model': 'land.info',
            'view_mode': 'list,form',  # Odoo 18 uses list
            'domain': [('owner_id', '=', self.id)],
            'context': {'default_owner_id': self.id},
        }

    def action_confirm(self):
        self.state = 'active'

    def action_inactive(self):
        self.state = 'inactive'

    def action_reset_to_draft(self):
        self.state = 'draft'