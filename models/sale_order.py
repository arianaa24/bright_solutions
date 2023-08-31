from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    precio_unitario_dias = fields.Float(string="Precio unitario por día", related="product_template_id.list_price", readonly=False)
    
    @api.onchange("x_studio_das")
    def _onchange_price(self):
        self.price_unit = self.product_uom_qty * self.x_studio_das * self.precio_unitario_dias