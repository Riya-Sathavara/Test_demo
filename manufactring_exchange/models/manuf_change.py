
from openerp import models, fields, api


from openerp import tools
from openerp import SUPERUSER_ID



class mrp_production(models.Model):
   
    _inherit = 'mrp.production'


class data(models.Model):
    _name = 'manu.data'
#     _inherits = { 'credential.task' : "**task_id**" }
     
    name = fields.Char(stirng = "Name")
    task_id = fields.One2many('demo.credential','task_id',string = "Task")
    
class sale_order_line(models.Model):
    _inherit = 'sale.order.line'    
    
    @api.onchange('note')
    def onchange_note(self):
        
        print ""
        return True

    @api.onchange('product_id')
    def product_id_change_with_wh(self):
        
#         res = super( sale_order_line, self).product_id_change_with_wh()
        print ""  
        return {}

#     def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
#             uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#             lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, warehouse_id=False, context=None):
#         context = context or {}
#         product_uom_obj = self.pool.get('product.uom')
#         product_obj = self.pool.get('product.product')
#         warning = {}
# 
#         return {}


# class Credential(models.Model):
#    
#     _inherits = ['mail.thread']