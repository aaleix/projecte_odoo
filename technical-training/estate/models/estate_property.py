from odoo import fields, models
from odoo import api
from odoo.exceptions import UserError
from datetime import datetime,timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    name = fields.Char('Nom', required=True)
    description = fields.Text('Descripció')
    postcode = fields.Char('Codi Postal')
    date_availability = fields.Date('Data de disponibilitat', copy=False, default=lambda self: (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d'))
    selling_price = fields.Float('Preu de venda esperat')
    selling_price_1 = fields.Float('Preu de venda', copy=False, store=True, compute='_compute_selling_price_1')
    bedrooms = fields.Integer('Nombre Habitacions', required=True)
    active = fields.Boolean(default=True)
    estat = fields.Selection([('New','Nova'), ('Offer Received', 'Oferta Rebuda'), ('Offer Accepted', 'Oferta Acceptada'), ('Sold', 'Venuda'), ('Canceled', 'Cancel·lada'), ],default='New')
    ascensor = fields.Selection([('No','No'), ('Yes', 'Sí'), ],default='No')
    parking = fields.Selection([('No','No'), ('Yes', 'Sí'), ],default='No')
    renovat = fields.Selection([('No','No'), ('Yes', 'Sí'), ],default='No')
    banys = fields.Integer('Banys')
    superficie = fields.Integer('Superfície', required=True)
    anyConstruccio = fields.Integer('Any de construcció')
    certificat_Energetic = fields.Selection([('A','A'), ('B','B'), ('C','C'), ('D','D'), ('E','E'), ('F','F'), ('G','G'), ])
    tipus_id = fields.Many2one('estate.property.categoria', string='Tipus')
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    buyer_id = fields.Many2one('res.partner', string='Comprador')
    salesperson_id = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user.id)
    offer_ids = fields.One2many('estate.property.offers', 'property_id', string='Ofertes')
    avgPrice = fields.Float('Preu per m2',compute='_calcular_preu_per_metre')
    ofertaMajor = fields.Float('Millor Oferta',compute='_trobar_oferta_mes_alta',stored=True)
    

    @api.depends('selling_price','superficie', 'offer_ids.preu', 'offer_ids.estat')
    def _compute_selling_price_1(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda offer: offer.estat == 'Accepted')
            if accepted_offer:
                record.selling_price_1 = accepted_offer.preu
            else:
                record.selling_price_1 = record.selling_price_1 or False

    @api.depends('selling_price','superficie')
    def _calcular_preu_per_metre(self):
        for record in self:
            if record.superficie > 0 :
                record.avgPrice = record.selling_price/record.superficie
            else:
                record.avgPrice = None
          
    @api.depends('offer_ids.preu')
    def _trobar_oferta_mes_alta(self):
        for property in self:
            ofertaMajor = max(
            (offer.preu for offer in property.offer_ids if offer.estat != 'Rejected'),
            default=0
        )
        property.ofertaMajor = ofertaMajor
    

    