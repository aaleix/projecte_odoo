from odoo import fields, models
class EstatePropertyCategoria(models.Model):
    _name = 'estate.property.categoria'
    name = fields.Char('Tipus')