
from odoo import fields, models


class LandType(models.Model):
    """A class for the model property facilities to represent
    the related facilities for a property"""
    _name = 'land.type'
    _description = 'Land Type'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)




class LandClassification(models.Model):
    """A class for the model property facilities to represent
    the related facilities for a property"""
    _name = 'land.classification'
    _description = 'Land Classification'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)




class LandUsage(models.Model):
    """A class for the model property facilities to represent
    the related facilities for a property"""
    _name = 'land.usage'
    _description = 'Land Usage'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)


class Division(models.Model):
    _name = 'res.division'
    _description = 'Division'

    name = fields.Char(string="Division Name", required=True)


class District(models.Model):
    _name = 'res.district'
    _description = 'District'

    name = fields.Char(string="District Name", required=True)

    division_id = fields.Many2one(
        'res.division',
        string="Division",
        required=True
    )


