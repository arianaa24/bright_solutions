from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    margen_total = fields.Float(string="Margen Total %")

    @api.onchange("order_line")
    def onchange_margen_total(self):
        total_vc = sum(line.vc for line in self.order_line)
        total_price_subtotal = sum(line.price_subtotal for line in self.order_line)
        self.margen_total = total_vc / total_price_subtotal if total_price_subtotal != 0 else 0

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dias = fields.Integer(string="Días")
    precio_unitario_dias = fields.Float(string="Precio unitario por día", digits=(12,2))
    costo_total = fields.Monetary(string="Costo Total")
    vc = fields.Monetary(string="VC")
    margen = fields.Float(string="Margen %")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.precio_unitario_dias = self.product_id.list_price

    @api.onchange("dias", "precio_unitario_dias","product_uom_qty")
    def _onchange_price(self):
        self.price_unit = self.dias * self.precio_unitario_dias

    @api.onchange("x_studio_costo","precio_unitario_dias", "product_uom_qty", "dias")
    def _onchange_product_id(self):
        self.costo_total = self.product_uom_qty * self.dias * self.x_studio_costo
        self.vc = self.price_subtotal - self.costo_total
        if self.price_subtotal:
            self.margen = self.vc / self.price_subtotal