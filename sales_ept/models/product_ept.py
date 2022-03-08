from odoo import fields,models,api

class Product_EPT(models.Model):
    _name="product.ept"
    _description="This model is part of sales and it is connected with product category and sales"

    category_id = fields.Many2one('product.category.ept', string="Product Category",
                                  help="Product will be categorized product category wise")
    name=fields.Char(string="Product Name", help="Product Name field of product.ept model")
    sku=fields.Char(string="SKU", help="Product sku field which is identify to particular product code wise")
    weight=fields.Float(string="Weight", help="To store weight of each product")
    length=fields.Float(string="Length", help="To store length of each product")
    volume=fields.Float(string="Volume", help="To store volume of each product")
    width=fields.Float(string="Width", help="To store width of each product")
    barcode=fields.Char(string="Barcode Character", help="To store character of barcode particular product wise")
    product_type = fields.Selection(selection=[('Storable', 'Storable'), ('Consumable', 'Consumable'), ('Service', 'Service')])
    sale_price = fields.Float(string="Sale Price", help="Sales price field of product model")
    cost_price=fields.Float(string="Purchase Price", help="Purchase price field of product model")
    uom_id = fields.Many2one('product.uom.ept', string="Unit", help="Unit for product will use in sales and purchase transaction")
    product_description=fields.Text(string="Description", help="Product description field of product model")
    product_stock = fields.Float(string="Current Stock", help="System will calculate current stock from all locations", store=False, compute="calculate_stock")

    def calculate_stock(self):
        stock_locations = self.env.context.get('location_id',False)
        if not stock_locations:
            stock_locations = self.env['stock.warehouse.ept'].search([]).stock_location_id.ids

        for product in self:
            product_quantity = 0
            stock_moves = self.env['stock.move.ept'].search([('product_id','=',product.id),('state', '=' , 'Done')])

            for stock_move in stock_moves:
                if stock_move.destination_location_id.id in stock_locations:
                    product_quantity += stock_move.qty_to_deliver
                elif stock_move.source_location_id.id in stock_locations:
                    product_quantity -= stock_move.qty_to_deliver
            product.product_stock = product_quantity

    def btn_action_update_stock(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("sales_ept.action_product_stock_update_ept")
        return action






