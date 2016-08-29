from openerp.osv import osv
from openerp.report import report_sxw


class inherit_purchase_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(inherit_purchase_report, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'test': self._test,
        })
        

    def _test(self,object):
    
        return "Testing Method"

class inherit_purchase_report_format(osv.AbstractModel):
    _name = 'report.purchase.report_purchaseorder'
    _inherit = 'report.abstract_report'
    _template = 'purchase.report_purchaseorder'
    _wrapped_report_class = inherit_purchase_report
