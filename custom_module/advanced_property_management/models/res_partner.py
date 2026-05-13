
from odoo import fields, models


class ResPartner(models.Model):
    """A class that inherits the already existing model res partner"""
    _inherit = 'res.partner'

    blacklisted = fields.Boolean(string='Blacklisted', default=False,
                                 help='Is this contact a blacklisted contact '
                                      'or not')

    def create(self, vals_list):
        """Make partner to blacklist"""
        val = super(ResPartner, self).create(vals_list)
        val.blacklisted = True
        return val

    def action_add_blacklist(self):
        """Sets the field blacklisted to True"""
        self.blacklisted = True

    def action_remove_blacklist(self):
        """Sets the field blacklisted to False"""
        self.blacklisted = False
