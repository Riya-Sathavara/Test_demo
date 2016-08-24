# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from openerp import models, fields, api
from _dbus_bindings import String
from chameleon.nodes import Default
from apt_pkg import DATE
from gdata.youtube import Age
from time import gmtime, strftime
from openerp import exceptions, SUPERUSER_ID, tools
from openerp.tools.translate import _
import datetime
from gi.overrides.Gtk import Editable
from bzrlib.transport import readonly
from email import _name
from openerp.exceptions import ValidationError
from _smbc import Context
from pygments.lexer import _inherit
from string import index
from bzrlib import api_minimum_version
from re import search

import xlsxwriter

class wizard(models.TransientModel):
    _name = 'demo.wizard'
    
    
    cred_id = fields.Many2one('demo.credential' , string="Name")       #for credential data
    wiz_dept = fields.Char(string="Department")
    wiz_position = fields.Char(string="Job Position")
    wiz_salary = fields.Integer(string="Salary")


    @api.multi
    def wizard_action_save(self):
        self.cred_id.salary = self.wiz_salary
        self.cred_id.dept = self.wiz_dept
        self.cred_id.position = self.wiz_position
        



class Credential(models.Model):
    _name = 'demo.credential'
    _inherit = ['mail.thread']
#     _inherits = {'mail.alias': 'alias_id'}
    
    name = fields.Char(string = "Name" , readonly = True , help = "That is useful for credential serial number." )
    age = fields.Char(string = "Age")
    date_join = fields.Date(string = "Date of joining")
    description = fields.Text(string = "Description")
    gender = fields.Selection([('Male','male'),('Female','Female')],string="Gender")
    dept = fields.Char(string="Department")
    position = fields.Char(string="Job Position")
    salary = fields.Integer(string="Salary")
    bod = fields.Date(string = "Date Of Birth")
    ima = fields.Binary(string = "Images")
    task_id = fields.Many2one('project.task', string = "Task")         # many2one field having always id
    sem1 = fields.Integer(string="Sem1")
    sem2 = fields.Integer(string = "Sem2")
    total = fields.Integer(string = "Total",compute='compute_total',store=True) #store the total value in database using store =true
    state = fields.Selection([('Draft','Draft'),('Approve','Approve'), ('progress', 'In progress'),('Done','Done')],default='Draft',string="State")
    warehouse_id = fields.Many2one('sale.order', string = "Warehouse")
    info_ids = fields.One2many('demo.info','credential_id',string="Information", states={'draft': [('readonly', False)], 'progress': [('readonly', False)]})
    us_data_ids = fields.Many2many('sale.order','demo_cre_sale','demo_credential_id','sale_order_id',string= "Demo" )
    # Many2Many create ids and first is module name , second module name that is a new table name that can automatically created then another argument is that table field name , that can be base on you 
    _defaults = {
                
            'date_join' : fields.Datetime.now,
            'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'demo.credential'),
              # For Serial Number generate in name field
                 
                }
    
    @api.depends('sem1','sem2') # when database update and change the sem1 or sem2 value change then compute the total that reason used
    def compute_total(self):
        self.total=self.sem1+self.sem2

    @api.multi
    def click_button_wizard_view(self):         #for wizard call this
         
        mod_obj = self.pool.get('ir.model.data')      # ir.model.data = all model data can be store in that id
        res_id = mod_obj.get_object_reference(self._cr, self._uid, 'demo', 'wizard_view_wizard_form')       # 'demo' = that is my module name demo
        return {
            'name':_("Test Wizard"),
            'type': 'ir.actions.act_window',
            'res_model': 'demo.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': res_id[1],
             
#             'res_id': res_id[1],
#             'nodestroy': True,
            'target': 'new',          # new = Pop up crsale.view_order_formeated ,  current  = pop up not open simple form can be open
#             'views': [(False, 'form'),  # open default form view first,
#               (False, 'tree')]  # then default tree view
 
#             'domain': '[]',
#             'context': dict(context, active_ids=ids)
        }
#         
    @api.multi
    def get_data(self):
                                      
 
        vals = {
                 
                'name' : "DO0100",
                'age' : "21",
                'bod': "01/25/1995"
                  
            }
        cred_id = self.env['demo.credential'].create(vals)
         
        vals = {
             'f_name':"sfcxx",
             'm_name' : "fdsff",
             'email' : "yfcsd",
             'credential_id' : cred_id.id
            }
        data = self.env['demo.info'].create(vals)
             
        return True
    
    
    
    
    @api.multi
    def action_draft(self):
        return True
    
    @api.multi
    def unlink(self):
        for data in self:
            if data.state is ("Done"):
                raise exceptions.Warning(_('You cannot delete the data in Done State'))
#             elif invoice.internal_number:
#                 raise Warning(_('You cannot delete an invoice after it has been validated (and received a number).  You can set it back to "Draft" state and modify its content, then re-confirm it.'))
        return super(Credential, self).unlink()

    @api.multi
    def copy(self,vals):
#         if default is self:
        
        vals.update({'name': False})
            
        return super(Credential, self).copy(vals) # Super is used to call another module method 
    
    
    @api.onchange('bod')
    def onchange_age_count(self):
        if self.bod:
            current_time = datetime.datetime.now()
            birth_time = datetime.datetime.strptime(self.bod,"%Y-%m-%d")
            age = current_time.year - birth_time.year 
            self.age = age
            
            if age <= 0:
                self.age = 0.0
                return { 'warning' : {
                    'title': _('Warning!'),
                    'message': _('Please enter valid Birth Date'),
                } } 
            
            elif age < 15:
                     
                    raise ValidationError("Please Enter Correct Birth Date : %s (user Name)" %self.name)    
                
            else:
                self.age =  int(age)
                
    @api.one
    @api.constrains('age')
    def _check_age(self):           
                
#         if int(self.age) < 20:
#             raise ValidationError("Please Enter correct Birth Date : %s" % self.name)
        return True
#                 print "hellooooo"
#                 val = {
#                         'age': age
#                         print "heeeeeeeeee"
#                         }
#                 return {'value': val}
#                 raise exceptions.Warning(_('Please Insert valid Birth date of User name:%s')%self.name)
                
    @api.one
    def concept_progressbar(self):
        self.write({
                    'state': 'Draft',
                    })       
        
    
    
    @api.multi
    def approve_progressbar(self):
        self.write({'state' : 'Approve'})
    
        return True
    
    @api.one
    def proces_progressbar(self):
        self.write({
                    'state': 'progress'
                    })
        
    @api.one
    def done_progressbar(self):
        self.write({
                    'state': 'Done'
                    })
    
    

    
#     def _check_names(self,cr, uidplanned_hours, ids, context=None):
#         for self_obj in self.browse(cr,uid,ids,context = context):
#             print self_obj.name
# #             credential_ids = self.search(cr,uid,[])
# #             for obj_name in self.browse(cr,uid,credential_ids):
# #                 if obj_name.name != self_obj.age:
# #                     return False
#             return True
        
        
        
        #       Constrains use       
    @api.one
    @api.constrains('name')
    def _check_name(self):
         
        self._cr.execute("""SELECT id FROM demo_credential WHERE name = '%s'"""%(self.name))
        cre_ids = self._cr.fetchall() 
#         data = self.search([ ('id', '=' , self.id)])
    
         
#         cred_ids = self.search([('id','<>',self.id),('name','=',self.name)])      # ('id','<>',self.id)  = using that Domain current create new id can be get
#         for cred_id in cred_ids:
#             if cred_id.name == self.name AND cred_id.id != self.id:      # And is used for operations if both statements are true then raise error ... ANd  otherwise create new record
#                 
#                 raise ValidationError("Fields name  must be different")
#          
#         return True
##### that is not not used in version 8
#     _constraints = [
#         (_check_names, 'That user Already Exists.', ['name']),
# 
#     ]

class information(models.Model):
    _name='demo.info'
    
    f_name = fields.Char(string = "Father Name")
    m_name = fields.Char(string = "Mother Name")
    email = fields.Char(string="Email-id")
    credential_id = fields.Many2one('demo.credential')

     
class task(models.Model):
    _inherit = 'project.task'
         
         
    date_join = fields.Integer(string = "Date of joining")
    task_ids = fields.One2many('demo.credential', 'task_id',string="Task") 
    #in one2many field having always & Many2many field having ids
    

class procurement_order(models.Model):
    _inherit = 'procurement.order'
# class sale_order(models.Model):
#     _inherit = 'sale.order' 

    @api.model
    def create(self, vals):
        res = super(procurement_order, self).create(vals)     
        # super = when we use super you can use another module function and change it  
#         1. override : then new function call old function not worked 2. inherit : then use that function and change in that but first call old function then new
         
        return res
    
class sale_order(models.Model):
    _inherit = 'sale.order' 
      
    @api.model
    def create(self , vals):
        sale = super(sale_order,self).create(vals)
         
        return sale
          
class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
     
    @api.model
    def create(self,value):   
        sale_order = super(sale_order_line,self).create(value)
          
        return sale_order
        