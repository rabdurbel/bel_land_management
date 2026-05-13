from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class BuildingInfo(models.Model):
    _name = 'building.info'
    _description = 'Building Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'building_name'
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True,
                       copy=False, default='New',
                       help='The reference code/sequence of the property Building Information')
    owner_id = fields.Many2one('property.owner', string='Owner', tracking=True)
    land_id = fields.Many2one('land.info', string='Land Reference')
    building_name = fields.Char(string='Building Name', tracking=True)
    plot_address = fields.Text(string='Plot Address')
    total_floor = fields.Integer(string='Total Floor')
    year_of_construction = fields.Char(string='Year of Construction')

    building_image = fields.Binary(string="Image", help="Image of the Land")

    OCCUPANCY_STATUS = [
        ('occupied', 'Occupied'),
        ('vacant', 'Vacant'),
        ('partial', 'Partially Occupied'),

    ]

    occupancy_status = fields.Selection(OCCUPANCY_STATUS, string='Occupancy Status')
    plot_size_sft = fields.Float(string='Plot Size (SFT)')
    total_basement = fields.Integer(string='Total Basement', default=0)

    # ✅ Status List
    BUILDING_STATUS = [
        ('draft', 'Draft'),
        ('under_construction', 'Under Construction'),
        ('completed', 'Completed'),
        ('renovation', 'Under Renovation'),
        ('cancel', 'Cancelled')
    ]

    # ✅ Field
    building_status = fields.Selection(
        BUILDING_STATUS,
        string='Building Status',
        default='draft',  # 👉 better start from draft
        tracking=True
    )

    generator_info = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Generator Information', default='no')

    rent_agreement_attachment = fields.Binary(string='Rent Agreement Attachment', attachment=True)


    # ✅ Button Actions
    def action_start_construction(self):
        for rec in self:
            rec.building_status = 'under_construction'

    def action_complete(self):
        for rec in self:
            rec.building_status = 'completed'

    def action_cancel(self):
        for rec in self:
            rec.building_status = 'cancel'

    def action_reset(self):
        for rec in self:
            rec.building_status = 'draft'



    def action_renovation(self):
        for rec in self:
            rec.building_status = 'renovation'




    # Relations
    # rental_info_ids = fields.One2many('rental.info', 'building_id', string='Rental Information')
    # rental_collection_ids = fields.One2many('rental.collection', 'building_id', string='Rental Collections')
    # maintenance_ids = fields.One2many('maintenance.utility', 'building_id', string='Maintenance Records')
    # bank_loan_ids = fields.One2many('bank.loan', 'building_id', string='Bank Loans')

    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('building.info') or '00001'
            vals['name'] = f"BUIL/{year}/{month_name}/{seq}"
        return super(BuildingInfo, self).create(vals)

    @api.constrains('total_floor', 'total_basement')
    def _check_floors(self):
        for record in self:
            if record.total_floor <= 0:
                raise ValidationError(_('Total floor must be greater than zero!'))
            if record.total_basement < 0:
                raise ValidationError(_('Total basement cannot be negative!'))
