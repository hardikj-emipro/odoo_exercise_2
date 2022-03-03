from odoo import fields,models,api

class Stock_Warehouse(models.Model):
    _name="stock.warehouse.ept"
    _description="Warehouse"

    name=fields.Char(string="Warehouse Name", required=True, help="Name of warehouse")
    short_code=fields.Char(string="Code", required=True, help="Code for warehouse")
    address_id=fields.Many2one(comodel_name="res.partner.ept", string="Address", help="Address data will come from "
                                                                                     "partner model")
    stock_location_id=fields.Many2one(comodel_name="stock.location.ept", string="Stock Location",
                                     help="Locations for warehouse", domain="[('location_type','=','Internal')]")
    view_location_id=fields.Many2one(comodel_name="stock.location.ept", string="View Location",
                                    help="view location",domain="[('location_type','=','View')]")

    @api.model
    def create(self,vals):
        stock_location = self.env['stock.location.ept']
        tmp_dict1 = {
            "name":"View Location",
            "parent_id": False,
            "location_type": "View",
            "is_scrap_location": False
        }
        last_inserted_record1 = stock_location.create(tmp_dict1)
        tmp_dict2 = {
            "name": "Stock Location",
            "parent_id": last_inserted_record1.id,
            "location_type": "Internal",
            "is_scrap_location": False
        }
        last_inserted_record2 = stock_location.create(tmp_dict2)
        vals.update({"stock_location_id": last_inserted_record2.id,
                                "view_location_id": last_inserted_record1.id})
        last_inserted_record2 = super(Stock_Warehouse, self).create(vals)
        # last_inserted_record2 = super(Stock_Warehouse, self).create({
        #                         "name":vals.get('name'),
        #                         "short_code":vals.get('short_code'),
        #                         "address_id": vals.get('address_id'),
        #                         "stock_location_id": last_inserted_record2.id,
        #                         "view_location_id": last_inserted_record1.id
        #                                      })
        return  last_inserted_record2



