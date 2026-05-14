from odoo import fields, models

class MouzaName(models.Model):
    """A class for the model property facilities to represent
    the related facilities for a property"""
    _name = 'mouza.name'
    _description = 'Mouza Name'
    _rec_name = 'name'

    name = fields.Char(string='Name',help='Mouza Name of the property')
