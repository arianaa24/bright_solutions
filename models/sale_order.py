from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dias = fields.Integer(string="Días")
    precio_unitario_dias = fields.Float(string="Precio unitario por día")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.precio_unitario_dias = self.product_id.list_price

    @api.onchange("dias", "precio_unitario_dias")
    def _onchange_price(self):
        self.price_unit = self.dias * self.precio_unitario_dias