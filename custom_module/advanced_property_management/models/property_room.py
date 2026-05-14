from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

selection_level = [("p", "P"), ("m", "M"), ("s", "S")] + [(str(num), str(num)) for num in range(1, 30)]


class PropertyRoom(models.Model):
    _name = "property.room"
    _description = "Room"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id desc'

    reference = fields.Char(string='Reference', readonly=True,
                       copy=False, default='New',
                       help='The reference code/sequence of the property Land Info')
    name = fields.Char(string="Number")
    property_id = fields.Many2one("property.property", string="Property", required=True)

    # property_id = fields.Many2one(
    #     'property.property', string='Property',
    #     required=True, copy=False,
    #     help='The property to be rented',
    #     domain="[('state','=','available'),('sale_rent','=','for_tenancy')]")

    level = fields.Selection(selection_level)

    height = fields.Float()
    perimeter = fields.Float()
    surface_disinsection = fields.Float(
        string="Area of disinsection",
        compute="_compute_surface_disinsection",
        store=True,
    )

    surface = fields.Float("Surface area")
    surface_cleaning_floor = fields.Float(string="Surface cleaning floor")
    surface_cleaning_doors = fields.Float(string="Surface cleaning doors")
    surface_cleaning_windows = fields.Float(string="Surface cleaning window")

    floor_type = fields.Selection([("c", "Carpet"), ("l", "Linoleum"), ("w", "Wood")])

    room_type = fields.Selection([
        ('bedroom', 'Bedroom'),
        ('living', 'Living Room'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('other', 'Other'),
    ], string="Room Type")

    # ✅ STATUS/STATE
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Verification'),
        ('approve', 'Approved'),
        ('done', 'Active'),
        ('cancel', 'Cancelled'),
    ], string="Status", default='draft', tracking=True)

    # 🔹 ACTION METHODS
    def action_verify(self):
        self.state = 'verify'

    def action_approve(self):
        self.state = 'approve'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_reset_draft(self):
        if self.state == 'cancel':
            self.state = 'draft'

    usage = fields.Selection(
        [
            ("office", "Office"),
            ("meeting", "Meeting room"),
            ("kitchen", "Kitchen"),
            ("laboratory", "Laboratory"),
            ("garage", "Garage"),
            ("archive", "Archive"),
            ("warehouse", "Warehouse"),
            ("log_warehouse", "Logistics warehouse"),
            ("it_endowments", "IT endowments (Ranks, Hall Servers)"),
            (
                "premises",
                "Technical premises (thermal, air conditioning, post-transformer)",
            ),
            ("cloakroom", "Cloakroom"),
            ("sanitary", "Sanitary group"),
            ("access", "Access ways"),
            ("lobby", "Lobby"),
            ("staircase", "Staircase"),
            ("living", "Living Room"),
            ("bedroom", "Bedroom"),
            ("balcony", "Balcony"),
        ],
        string="Room usage",
        help="The purpose of using the room",
        default="bedroom",
    )
    usage_id = fields.Many2one("room.usage", string="Room usage", help="The purpose of using the room")

    rented_room = fields.Boolean()
    tenant_id = fields.Many2one("res.partner", string="Tenant")

    last_maintenance = fields.Date()
    technical_condition = fields.Selection(
        [("0", "Missing"), ("1", "Unsatisfactory"), ("3", "good"), ("5", "very good")],
        aggregator="avg",
    )

    @api.model_create_multi
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('property.room') or '00001'
            vals['reference'] = f"PR/{year}/{month_name}/{seq}"
        return super(PropertyRoom, self).create(vals)

    @api.depends("surface", "height", "perimeter")
    def _compute_surface_disinsection(self):
        for room in self:
            room.surface_disinsection = 2 * room.surface + room.height * room.perimeter

    @api.constrains
    def _check_cleaning_surface(self):
        if self.cleaning_surface > self.surface:
            raise ValidationError(_("Cleaning surface most by lower that surface area"))


class RoomUsage(models.Model):
    _name = "room.usage"
    _description = "Room usage"

    name = fields.Char(string="Usage")
