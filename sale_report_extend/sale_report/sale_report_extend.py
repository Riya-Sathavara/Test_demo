import string
from openerp.osv import osv
from openerp.report import report_sxw



class sale_extend_data(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_extend_data, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'demo': self._demo,
            'dot': self._dot,
            'sub_total' : self._sub_total,
         
        })
        

    def _demo(self,object):
        list = []
        for line in object.order_line:
            list.append(line.product_id.name)
        return list
    
    def _dot(self,object):
#             data_obj = str(object.price_unit)
            temp = string.split(str(object.price_unit),".")
            dot = temp[0] + ','+ temp[1]
            return dot
        
    def _sub_total(self,object):
        sub_total= 0
        for line in object.order_line:
                sub_total += line.price_subtotal 
        return sub_total

    
class credential_report_sale_ext(osv.AbstractModel):
    _name = 'report.sale_report_extend.sale_data_report'
    _inherit = 'report.abstract_report'
    _template = 'sale_report_extend.sale_data_report'
    _wrapped_report_class = sale_extend_data
    
    
    
    
