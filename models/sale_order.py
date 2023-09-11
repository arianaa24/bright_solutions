from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dias = fields.Integer(string="Días")
    precio_unitario_dias = fields.Float(string="Precio unitario por día")
    costo_total = fields.Monetary(string="Costo Total")
    vc = fields.Monetary(string="VC")
    margen = fields.Float(string="Margen %")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.precio_unitario_dias = self.product_id.list_price

    @api.onchange("dias", "precio_unitario_dias")
    def _onchange_price(self):
        self.price_unit = self.dias * self.precio_unitario_dias

    @api.onchange("x_studio_costo")
    def _onchange_product_id(self):
        self.costo_total = self.product_uom_qty * self.dias * self.x_studio_costo
        self.vc = self.price_subtotal - self.costo_total
        self.margen = self.vc / self.price_subtotal