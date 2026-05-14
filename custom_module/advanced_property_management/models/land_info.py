from odoo import models, fields, api, _
from datetime import datetime


class LandInfo(models.Model):
    _name = 'land.info'
    _description = 'Land Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'land_name'
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True,
                       copy=False, default='New',
                       help='The reference code/sequence of the property Land Info')

    land_name = fields.Char(string='Project Area', required=True, tracking=True)
    owner_id = fields.Many2one('property.owner', string='Owner', required=True, tracking=True)
    image = fields.Binary(string="Image", help="Image of the Land")
    user_id = fields.Many2one(
        'res.users',
        string="Owner",
        default=lambda self: self.env.user
    )

    KHATIAN_TYPE = [
        ('cs', 'CS'),
        ('rs', 'RS'),
        ('sa', 'SA'),
        ('bs', 'BS'),
    ]

    khatian_no = fields.Selection(KHATIAN_TYPE,string='Khatian No')
    khatian_no_cs = fields.Char(string='Khatian No CS')
    khatian_no_rs = fields.Char(string='Khatian No RS')
    khatian_no_sa = fields.Char( string='Khatian No SA')
    khatian_no_bs = fields.Char(string='Khatian No BS')
    total_land_area = fields.Float(string='Total Land Area (in decimal)', required=True, tracking=True)
    land_management = fields.Char(string='Land Management')
    district = fields.Char(string='District', required=True)

    division_id = fields.Many2one(
        'res.division',
        string="Division"
    )

    district_id = fields.Many2one(
        'res.district',
        string="District"
    )
    thana = fields.Char(string='Thana', required=True)
    land_occupied = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Land Occupied', required=True, default='no')

    land_location_map = fields.Binary(string='Land Location Map', attachment=True)
    mouza_name = fields.Many2one('mouza.name',string='Mouza Name')
    plot_dag_no = fields.Char(string='Plot/Dag NO (AS Per Record)')
    plot_dag_cs = fields.Char(string='Plot/Dag NO CS')
    plot_dag_rs = fields.Char(string='Plot/Dag NO RS')
    plot_dag_sa = fields.Char(string='Plot/Dag NO SA')
    plot_dag_bs = fields.Char(string='Plot/Dag NO BS')

    total_land_dag = fields.Float(string='Total Land/Dag')
    purchase_land_area = fields.Float(string='Purchase Land Area (Decimal)')
    deed_no =fields.Char(string='Deed No', tracking=True)
    date = fields.Date(string='Date')
    viya_deed = fields.Char(string='Bia Deed')
    viya_mutation = fields.Char(string='Bia Mutation')
    viya_court_order = fields.Char(string='Bia Court Order')
    other_document = fields.Binary(string='Other Document')


    khatian_no_cs_doc = fields.Binary(string="CS Document", attachment=True)
    khatian_no_rs_doc = fields.Binary(string="RS Document", attachment=True)
    khatian_no_sa_doc = fields.Binary(string="SA Document", attachment=True)
    khatian_no_bs_doc = fields.Binary(string="BS Document", attachment=True)

    # =========================
    # Plot / Dag Documents
    # =========================
    plot_dag_cs_doc = fields.Binary(string='Plot/Dag No CS')
    plot_dag_rs_doc = fields.Binary(string='Plot/Dag No RS')
    plot_dag_sa_doc = fields.Binary(string='Plot/Dag No SA')
    plot_dag_bs_doc = fields.Binary(string='Plot/Dag No BS')

    # =========================
    # Viya Documents
    # =========================
    viya_deed_doc = fields.Binary(string='Bia Deed')
    viya_mutation_doc = fields.Binary(string='Bia Mutation')
    viya_court_order_doc = fields.Binary(string='Bia Court Order')


    # MULTIPLE FILE (Attachment)
    # -------------------------
    viya_deed_doc_ids = fields.Many2many(
        'ir.attachment',
        'viya_deed_rel',
        'res_id',
        'attachment_id',
        string='Bia Deed'
    )

    viya_mutation_doc_ids = fields.Many2many(
        'ir.attachment',
        'viya_mutation_rel',
        'res_id',
        'attachment_id',
        string='Bia Mutation'
    )

    viya_court_order_doc_ids = fields.Many2many(
        'ir.attachment',
        'viya_court_rel',
        'res_id',
        'attachment_id',
        string='Bia Court Order'
    )




    LAND_TYPE = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('agricultural', 'Agricultural'),
        ('mixed', 'Mixed'),
    ]

    land_type = fields.Many2one('land.type', string='Land Type', required=True)
    division = fields.Char(string='Division', required=True)

    LAND_CLASSIFICATION = [
        ('urban', 'Urban'),
        ('rural', 'Rural'),
        ('semi_urban', 'Semi-Urban'),
    ]

    land_classification = fields.Many2one('land.classification', string='Land Classification')

    LAND_USAGE = [
        ('self_occupied', 'Self Occupied'),
        ('rented', 'Rented'),
        ('vacant', 'Vacant'),
        ('under_development', 'Under Development'),
    ]

    land_usage = fields.Many2one('land.usage', string='Land Usage', required=True)
    special_note = fields.Text(string='Special Note')

    # Relations
    land_tax_ids = fields.One2many('land.tax', 'land_id', string='Land Tax Information')
    building_structure_ids = fields.One2many('building.structure', 'land_id', string='Building Structures')
    building_ids = fields.One2many('building.info', 'land_id', string='Buildings')
    mutation_ids = fields.One2many('land.mutation.info', 'land_mutation_id', string='Mutation Info')

    case_ids = fields.One2many('case.pending.info', 'land_case_id', string='Cases')
    # attachment_ids = fields.Binary("Attachment", required=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")

    active = fields.Boolean(string='Active', default=True)

    # ================= COUNT FIELDS =================
    land_tax_count = fields.Integer(compute="_compute_counts")
    building_structure_count = fields.Integer(compute="_compute_counts")
    building_count = fields.Integer(compute="_compute_counts")
    case_count = fields.Integer(compute="_compute_counts")
    mutation_count = fields.Integer(compute="_compute_counts")


    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Verified'),
        ('approve', 'Approved'),
        ('done', 'Closed'),
    ], string="Status", default='draft', tracking=True)

    #  Count field
    doc_count = fields.Integer(string="Documents", compute="_compute_attached_docs")

    @api.onchange('division_id')
    def _onchange_division_id(self):
        if self.division_id:
            return {
                'domain': {
                    'district_id': [('division_id', '=', self.division_id.id)]
                }
            }
        else:
            return {
                'domain': {
                    'district_id': []
                }
            }


    #  Create attachment function
    def _create_attachment(self, field_name):
        for record in self:
            file_data = record[field_name]

            if file_data:
                # Avoid duplicate (optional check)
                existing = self.env['ir.attachment'].search([
                    ('res_model', '=', record._name),
                    ('res_id', '=', record.id),
                    ('name', '=', field_name)
                ], limit=1)

                if not existing:
                    self.env['ir.attachment'].create({
                        'name': field_name,
                        'type': 'binary',
                        'datas': file_data,
                        'res_model': record._name,
                        'res_id': record.id,
                    })

    # LINK MULTIPLE FILES
    def _link_multi_attachments(self, vals):
        multi_fields = [
            'viya_deed_doc_ids',
            'viya_mutation_doc_ids',
            'viya_court_order_doc_ids'
        ]

        for field in multi_fields:
            if field in vals:
                commands = vals.get(field)

                attachment_ids = []

                for command in commands:
                    # (6, 0, [ids]) → replace all
                    if command[0] == 6:
                        attachment_ids.extend(command[2])

                    # (4, id) → add existing
                    elif command[0] == 4:
                        attachment_ids.append(command[1])

                if attachment_ids:
                    attachments = self.env['ir.attachment'].browse(attachment_ids)

                    for rec in self:
                        attachments.write({
                            'res_model': rec._name,
                            'res_id': rec.id
                        })

    # ================= DELETE REMOVED ATTACHMENTS =================
    def _delete_removed_attachments(self, vals):
        multi_fields = [
            'viya_deed_doc_ids',
            'viya_mutation_doc_ids',
            'viya_court_order_doc_ids'
        ]

        for field in multi_fields:
            if field in vals:
                commands = vals.get(field)

                for rec in self:
                    old_ids = rec[field].ids
                    new_ids = []

                    for command in commands:
                        # (6, 0, [ids]) → replace all
                        if command[0] == 6:
                            new_ids = command[2]

                        # (4, id) → add
                        elif command[0] == 4:
                            new_ids.append(command[1])

                        # (3, id) → remove one
                        elif command[0] == 3:
                            if command[1] in old_ids:
                                self.env['ir.attachment'].browse(command[1]).unlink()

                        # (5) → remove all
                        elif command[0] == 5:
                            self.env['ir.attachment'].browse(old_ids).unlink()

                    # Handle replace case → delete missing ones
                    if commands and commands[0][0] == 6:
                        removed_ids = list(set(old_ids) - set(new_ids))
                        if removed_ids:
                            self.env['ir.attachment'].browse(removed_ids).unlink()

    #  Override create
    def create(self, vals):
        record = super().create(vals)
        record._create_attachment('khatian_no_cs_doc')
        record._create_attachment('khatian_no_rs_doc')
        record._create_attachment('khatian_no_sa_doc')
        record._create_attachment('khatian_no_bs_doc')
        record._create_attachment('plot_dag_cs_doc')
        record._create_attachment('plot_dag_rs_doc')
        record._create_attachment('plot_dag_sa_doc')
        record._create_attachment('plot_dag_bs_doc')
        # record._create_attachment('viya_deed_doc')
        # record._create_attachment('viya_mutation_doc')
        # record._create_attachment('viya_court_order_doc')
        record._link_multi_attachments(vals)
        return record

    #  Override write
    def write(self, vals):
        self._delete_removed_attachments(vals)  #  IMPORTANT
        res = super().write(vals)
        self._create_attachment('khatian_no_cs_doc')
        self._create_attachment('khatian_no_rs_doc')
        self._create_attachment('khatian_no_sa_doc')
        self._create_attachment('khatian_no_bs_doc')
        self._create_attachment('plot_dag_cs_doc')
        self._create_attachment('plot_dag_rs_doc')
        self._create_attachment('plot_dag_sa_doc')
        self._create_attachment('plot_dag_bs_doc')
        # self._create_attachment('viya_deed_doc')
        # self._create_attachment('viya_mutation_doc')
        # self._create_attachment('viya_court_order_doc')
        self._link_multi_attachments(vals)
        return res

    # Count attachments
    def _compute_attached_docs(self):
        for record in self:
            record.doc_count = self.env['ir.attachment'].search_count([
                ('res_model', '=', record._name),
                ('res_id', '=', record.id)
            ])

    # Open attachment view
    def attachment_tree_view(self):
        self.ensure_one()
        return {
            "name": _("Documents"),
            "type": "ir.actions.act_window",
            "res_model": "ir.attachment",
            "view_mode": "kanban,list,form",
            "domain": [
                ("res_model", "=", self._name),
                ("res_id", "=", self.id)
            ],
        }

    @api.model_create_multi
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            now = datetime.now()
            year = now.strftime('%Y')
            month_name = now.strftime('%b')  # JAN, FEB, MAR, SEP, OCT
            seq = self.env['ir.sequence'].next_by_code('land.info') or '00001'
            vals['name'] = f"BEL/{year}/{month_name}/{seq}"
        return super(LandInfo, self).create(vals)

    def action_verify(self):
        for rec in self:
            rec.state = 'verify'

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'

    # ================= COMPUTE =================
    def _compute_counts(self):
        for rec in self:
            rec.land_tax_count = self.env['land.tax'].search_count([
                ('land_id', '=', rec.id)
            ])
            rec.building_structure_count = self.env['building.structure'].search_count([
                ('land_id', '=', rec.id)
            ])
            rec.building_count = self.env['building.info'].search_count([
                ('land_id', '=', rec.id)
            ])
            rec.case_count = self.env['case.pending.info'].search_count([
                ('land_case_id', '=', rec.id)
            ])

            rec.mutation_count = self.env['land.mutation.info'].search_count([
                ('land_mutation_id', '=', rec.id)
            ])

    # ================= ACTIONS =================
    def action_view_land_tax(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Land Tax',
            'res_model': 'land.tax',
            'view_mode': 'list,form',
            'domain': [('land_id', '=', self.id)],
            'context': {'default_land_id': self.id},
        }

    def action_view_building_structure(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Building Structures',
            'res_model': 'building.structure',
            'view_mode': 'list,form',
            'domain': [('land_id', '=', self.id)],
        }

    def action_view_building(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Buildings',
            'res_model': 'building.info',
            'view_mode': 'list,form',
            'domain': [('land_id', '=', self.id)],
        }

    def action_view_case(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cases',
            'res_model': 'case.pending.info',
            'view_mode': 'list,form',
            'domain': [('land_case_id', '=', self.id)],
        }

    def action_view_mutation(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Mutations',
            'res_model': 'land.mutation.info',
            'view_mode': 'list,form',
            'domain': [('land_mutation_id', '=', self.id)],
        }



