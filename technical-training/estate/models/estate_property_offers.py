from odoo import fields, models
from odoo import api
class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    preu = fields.Float('Preu')
    estat = fields.Selection([('Accepted','Acceptada'), ('Rejected', 'Rebutjada'), ('In treatment', 'En tractament'),],default='In treatment', required=True)
    comprador = fields.Many2one('res.partner', string='Comprador')
    comentaris = fields.Text('Comentaris')
    property_id = fields.Many2one('estate.property', string='Propietat')

    @api.model
    def create(self, vals):
        offer = super(EstatePropertyOffers, self).create(vals)
        if offer.estat == 'Accepted':
            offer.update_property_fields()
        return offer

    def write(self, vals):
        result = super(EstatePropertyOffers, self).write(vals)
        for offer in self:
            if 'estat' in vals and vals['estat'] == 'Accepted':
                offer.update_property_fields()
        return result

    def update_property_fields(self):
        for offer in self:
            offer.property_id.write({
                'buyer_id': offer.comprador.id,
                'selling_price_1': offer.preu,
            })