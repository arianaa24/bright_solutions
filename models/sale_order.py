from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    precio_unitario_dias = fields.Float(string="Precio unitario por día")

    @api.onchange("product_id")
    def _onchange_product_id_para_precio(self):
        self.precio_unitario_dias = self.product_id.list_price

    @api.onchange("x_studio_das", "precio_unitario_dias")
    def _onchange_price_para_precio(self):
        self.price_unit = self.x_studio_das * self.precio_unitario_dias