from openerp.osv import osv
from openerp.report import report_sxw


class purchase_test_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(purchase_test_report, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'test': self._test,
        })
        

    def _test(self,object):
        
        return "testng alsdj"

class report_sale_invoice_ext(osv.AbstractModel):
    _name = 'report.test_qweb_report.purchase_test_report'
    _inherit = 'report.abstract_report'
    _template = 'test_qweb_report.purchase_test_report'
    _wrapped_report_class = purchase_test_report
    
    
    
    

