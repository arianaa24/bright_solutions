from odoo import api, fields, models, _
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    margen_total = fields.Float(string="Margen Total %")



    @api.onchange("order_line")
    def onchange_margen_total(self):
        total_vc = sum(line.vc for line in self.order_line)
        total_price_subtotal = sum(line.price_subtotal for line in self.order_line)
        self.margen_total = total_vc / total_price_subtotal if total_price_subtotal != 0 else 0
    
    def btn_calcular_monto_ejecutado(self):
        for so_line in self.order_line:
            purchase_order_lines = self.env['purchase.order.line'].search([('order_id.sale_order_id.id','=',self.id), ('state','=','purchase'), ('product_id.id','=',so_line.product_id.id)])
            so_line.monto_ejecutado = sum(purchase_order_lines.mapped('price_subtotal'))

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dias = fields.Integer(string="Días")
    precio_unitario_dias = fields.Float(string="Precio unitario por día", digits=(12,2))
    costo_total = fields.Monetary(string="Costo Total")
    vc = fields.Monetary(string="VC")
    margen = fields.Float(string="Margen %")
    monto_ejecutado = fields.Float(string="Monto Ejecutado")

    @api.onchange("product_id")
    def _onchange_product(self):
        self.precio_unitario_dias = self.product_id.list_price

    @api.onchange("dias", "precio_unitario_dias","product_uom_qty")
    def _onchange_price(self):
        self.price_unit = self.dias * self.precio_unitario_dias

    @api.onchange("x_studio_costo","precio_unitario_dias", "product_uom_qty", "dias")
    def _onchange_product_brighsolutions(self):
        for record in self:
            record.costo_total = record.product_uom_qty * record.dias * record.x_studio_costo
            record.vc = record.price_subtotal - record.costo_total
            if record.price_subtotal:
                record.margen = record.vc / record.price_subtotal
