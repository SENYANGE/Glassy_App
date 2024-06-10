
from turtle import textinput
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDRectangleFlatButton
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from zeroconf import re
from database import Database
import sqlite3
from kivymd.toast import toast
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.popup import Popup

Window.size=(350,580)
position =0
#-------------------SALES CLASSES------------------
class SlContents(FloatLayout):
    pass
#Adapter for customer recyclerview
class SlMyBL(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    #index = None
    def __init__(self, index=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.index = index
    
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    #index
    def get_selected(self):
        ''' Returns list of selected nodes dicts '''
        return [self.data[idx] for idx in self.layout_manager.selected_nodes]

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SlMyBL, self).refresh_view_attrs(
            rv, index, data)
   

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SlMyBL, self).on_touch_down(touch):
            
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            self.index = index
            print("selection changed to {0}".format(rv.data[index]))
            toast(str(rv.data[index]['sl_Quantity']))
            CustomerOptionsBox().open_diag()
            
        else:
            self.index = index
            print("selection removed for {0}".format(rv.data[index]))
            CustomerOptionsBox().popup_dismiss()
    def delete_customer(self):
        
                return self.ids.rv.get_selected()


#-----------------END OF SALES CLASESES------------------

#-------------------Purchases CLASSES------------------------
class PContents(FloatLayout):
    pass
#Adapter for customer recyclerview
class PMyBL(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    #index = None
    def __init__(self, index=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.index = index
    
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    #index
    def get_selected(self):
        ''' Returns list of selected nodes dicts '''
        return [self.data[idx] for idx in self.layout_manager.selected_nodes]

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(PMyBL, self).refresh_view_attrs(
            rv, index, data)
   

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(PMyBL, self).on_touch_down(touch):
            
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            self.index = index
            print("selection changed to {0}".format(rv.data[index]))
            toast(str(rv.data[index]['p_Quantity']))
            CustomerOptionsBox().open_diag()
            
        else:
            self.index = index
            print("selection removed for {0}".format(rv.data[index]))
            CustomerOptionsBox().popup_dismiss()
    def delete_customer(self):
        
                return self.ids.rv.get_selected()




#------------------END OF PURCHASES------------------------------
#expenses classes
#contents for logout dialog
class ExpContents(FloatLayout):
    pass
#Adapter for customer recyclerview
class ExpMyBL(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    #index = None
    def __init__(self, index=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.index = index
    
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    #index
    def get_selected(self):
        ''' Returns list of selected nodes dicts '''
        return [self.data[idx] for idx in self.layout_manager.selected_nodes]

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(ExpMyBL, self).refresh_view_attrs(
            rv, index, data)
   

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(ExpMyBL, self).on_touch_down(touch):
            
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            self.index = index
            print("selection changed to {0}".format(rv.data[index]))
            toast(str(rv.data[index]['cust_Name']))
            CustomerOptionsBox().open_diag()
            
        else:
            self.index = index
            print("selection removed for {0}".format(rv.data[index]))
            CustomerOptionsBox().popup_dismiss()
    def delete_customer(self):
        
                return self.ids.rv.get_selected()


#expenses classes
class CustomerOptionsBox(Popup):
    
    def popup_dismiss(self):
        self.dismiss()
    def open_diag(self):
        self.open()
        
#customer select box apearance
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,RecycleBoxLayout):
    pass
#Adapter for customer recyclerview
class MyBL(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    #index = None
    def __init__(self, index=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.index = index
    
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    #index
    def get_selected(self):
        ''' Returns list of selected nodes dicts '''
        return [self.data[idx] for idx in self.layout_manager.selected_nodes]

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(MyBL, self).refresh_view_attrs(
            rv, index, data)
   

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(MyBL, self).on_touch_down(touch):
            
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            self.index = index
            print("selection changed to {0}".format(rv.data[index]))
            toast(str(rv.data[index]['cust_Name']))
            CustomerOptionsBox().open_diag()
            
        else:
            self.index = index
            print("selection removed for {0}".format(rv.data[index]))
            CustomerOptionsBox().popup_dismiss()
    def delete_customer(self):
        
                return self.ids.rv.get_selected()
#contents for logout dialog
class Content(FloatLayout):
    pass
#contents for logout dialog
class UpdateCustomerContent(FloatLayout):
    
    pass
    


class Glassy(MDApp):
    dialog = None
    cus_dialog=None# logout dialog
    cus_update_dialog=None
    exp_dialog=None
    sl_dialog=None
    p_dialog=None
    def build(self):
        global screenmanager
        conn=Database()#connection to database
        
        screenmanager=ScreenManager()
        screenmanager.add_widget(Builder.load_file("splash.kv"))
        screenmanager.add_widget(Builder.load_file("login.kv"))
        screenmanager.add_widget(Builder.load_file("signup.kv"))
        screenmanager.add_widget(Builder.load_file("homepage.kv"))#homepage screen
        screenmanager.add_widget(Builder.load_file("purchases.kv"))
        screenmanager.add_widget(Builder.load_file("expenses.kv"))
        screenmanager.add_widget(Builder.load_file("sales.kv"))
        screenmanager.add_widget(Builder.load_file("customers.kv"))
        screenmanager.add_widget(Builder.load_file("remainder.kv"))
        return screenmanager
    
    def on_start(self):
        Clock.schedule_once(self.login_page,3)
    def login_page(self,*args):
            screenmanager.current='login'
     #delete customer *******************
    def delete_mycustomer(self):
        
        Database().delete_customer(self.root.get_screen('customers').ids.recycleview_id.data[position]['cust_ID'])
        CustomerOptionsBox().popup_dismiss()
        self.refresh_recycleview()
    #Update customer details
  
    def update_customer_confirmation_dialog(self):
        #UpdateCustomerContent().setFieldsText(self.root.get_screen('customers').ids.recycleview_id.data[position]['cust_Name'],self.root.get_screen('customers').ids.recycleview_id.data[position]['cust_Contact'])
        
        if not self.cus_update_dialog:
            self.cus_update_dialog = MDDialog(
                title="Update CUSTOMER",
                type="custom",
                content_cls=UpdateCustomerContent(),
                buttons=[
                    MDRectangleFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release= self.closeCustomerUpdateDialog
                    ),
                    MDRectangleFlatButton(
                        text="update", text_color=self.theme_cls.primary_color,on_release=self.Confirm_Update
                    ),
                ],
            )
        self.cus_update_dialog.content_cls.ids.up_cust_name.text=self.root.get_screen('customers').ids.recycleview_id.data[position]['cust_Name']
        self.cus_update_dialog.content_cls.ids.up_cust_phone.text=self.root.get_screen('customers').ids.recycleview_id.data[position]['cust_Contact']
        self.cus_update_dialog.open()
   
        # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('customers').ids.recycleview_id.data = self.data_from_dataset()
            
        #  ---- refresh the recycleview: ---- #
        self.root.get_screen('customers').ids.recycleview_id.refresh_from_data()

    #add customer dialog
    def add_customer_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="ADD CUSTOMER",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDRectangleFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release= self.closeDialog
                    ),
                    MDRectangleFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.add_mycustomer
                    ),
                ],
            )
        self.dialog.open()
   
        # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('customers').ids.recycleview_id.data = self.data_from_dataset()
            
        #  ---- refresh the recycleview: ---- #
        self.root.get_screen('customers').ids.recycleview_id.refresh_from_data()
    #all customers list
    def all_customers(self):
        return Database().all_customers()
    #data to add to recyclerview
    def data_from_dataset(self):
        rec= Database().all_customers()
        # ---- format your data for recycleview here ---- #
        records=[{'cust_ID': str(x[0]),'cust_Name':str(x[1]),'cust_Contact':str(x[2])} for x in rec]
        return records
    #refresh recyclerview
    def refresh_recycleview(self):
     # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('customers').ids.recycleview_id.data = self.data_from_dataset()
        
     #  ---- refresh the recycleview: ---- #
        self.root.get_screen('customers').ids.recycleview_id.refresh_from_data()

    #add customer method
    def add_mycustomer(self,inst):
        name=self.dialog.content_cls.ids.cust_name.text
        phone=self.dialog.content_cls.ids.cust_phone.text
        
        if name!='' and phone!='' :
            Database().add_customer(name,phone)
            toast(name +" added successfully!")
            self.refresh_recycleview()
            self.dialog.dismiss()
        elif name=='' and phone!='':
            toast("Enter name!")
        elif name!='' and phone=='':
            toast("Enter Phone!")  
        else:
            toast("Empty Field(s)!")
    
    #***********************************
    
    #confirm customer update
    def Confirm_Update(self,inst):
        c_name=self.cus_update_dialog.content_cls.ids.up_cust_name.text
        phone=self.cus_update_dialog.content_cls.ids.up_cust_phone.text 
        c_id=self.root.get_screen('customers').ids.recycleview_id.data[position]['cust_ID']
        if c_name!='' and phone!='' :
            Database().update_customer(c_name,phone,c_id) 
            toast(c_name +" updated successfully!")
            self.refresh_recycleview()
            self.cus_update_dialog.dismiss()
            c_name=''
            phone=''
            c_id=''
        elif c_name=='' and phone!='':
            toast("Enter name!")
        elif c_name!='' and phone=='':
            toast("Enter Phone!")  
        else:
            toast("Empty Field(s)!")
    #logout dialog
    def logout_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="LogOut",
                type="custom",
        
                buttons=[
                    MDRectangleFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release= self.closeDialog
                    ),
                    MDRectangleFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.logout_method
                    ),
                ],
            )
        self.dialog.open()
    
    def logout_method(self, inst):
        screenmanager.current='login'
        self.dialog.dismiss()

    def closeDialog(self, inst):
        self.dialog.dismiss() 
    def closeExpDialog(self, inst):
        self.exp_dialog.dismiss() 
    def closeCustomerDialog(self, inst):
        self.cus_dialog.dismiss() 
    def closeCustomerUpdateDialog(self, inst):
        self.cus_update_dialog.dismiss() 
    def closeSlDialog(self, inst):
        self.sl_dialog.dismiss() 
    def closePDialog(self, inst):
        self.p_dialog.dismiss() 
   #logout dialog ends 
   #signup page 
    def signup_back_login(self):
        screenmanager.current='login' 
    #login_method
    def login_method(self): 
        user = self.root.get_screen('login').ids.username_input.text
        pswd =self.root.get_screen('login').ids.pass_input.text
        #check if fields not empty
        if user and pswd is not None:
            #check if user is in Database
            if Database().verify_user(user,pswd)==1:
                screenmanager.current='homepage'
                Database().close_db_connection()
                self.root.get_screen('login').ids.username_input.text=''
                self.root.get_screen('login').ids.pass_input.text=''
                toast('Welcome '+user)
                self.root.get_screen('homepage').ids.username_tag.text=user
                self.root.get_screen('customers').ids.username_tag.text=user
                self.root.get_screen('purchases').ids.username_tag.text=user
                self.root.get_screen('expenses').ids.username_tag.text=user
                self.root.get_screen('sales').ids.username_tag.text=user
            else:
                toast('Invalid Password or Username')
    #signup method
    def signup_method(self):
        user = self.root.get_screen('signup').ids.username_s.text
        pswd =self.root.get_screen('signup').ids.password_s.text 
        pswd_c =self.root.get_screen('signup').ids.password_s_conf.text 
        if user =='' or None:
            toast("Enter Username")
        elif pswd=='' or None:
            toast("Enter Password")
        elif pswd_c =='' or None:
            toast("Re-Enter Password to continue")
        elif pswd !=pswd_c:
            toast("password mismatch")
        elif user !='' or user is not None and pswd !='' or pswd is not None and pswd==pswd_c:
            Database().create_user(user,pswd)
            self.root.get_screen('signup').ids.username_s.text=''
            self.root.get_screen('signup').ids.password_s.text=''
            self.root.get_screen('signup').ids.password_s_conf.text='' 
            toast("Account successfully done...")
            screenmanager.current='login'
#expenses functions           
    #add customer method
    def add_expenses(self,inst):
        expense_type=self.exp_dialog.content_cls.ids.exp_type.text
        exp_amount=self.exp_dialog.content_cls.ids.exp_amount.text
        
        if expense_type!='' and exp_amount!='' :
            Database().add_expense(expense_type,exp_amount)
            toast(expense_type +" added successfully!")
            self.refresh_recycleview()
            self.exp_dialog.dismiss()
        elif expense_type=='' and exp_amount!='':
            toast("Enter Expense Type!")
        elif expense_type!='' and exp_amount=='':
            toast("Enter Amount!")  
        else:
            toast("Empty Field(s)!")
    #add expense dialog
    def add_expense_confirmation_dialog(self):
        if not self.exp_dialog:
            self.exp_dialog = MDDialog(
                title="ADD Expense",
                type="custom",
                content_cls=ExpContents(),
                buttons=[
                    MDRectangleFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release= self.closeExpDialog
                    ),
                    MDRectangleFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.add_expenses
                    ),
                ],
            )
        self.exp_dialog.open()
   
        # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('expenses').ids.exp_rv.data = self.data_from_dataset_exp()
            
        #  ---- refresh the recycleview: ---- #
        self.root.get_screen('expenses').ids.exp_rv.refresh_from_data()
    #data to add to recyclerview
    def data_from_dataset_exp(self):
        rec= Database().all_expenses()
        # ---- format your data for recycleview here ---- #
        records=[{'exp_ID': str(x[0]),'exp_Type':str(x[1]),'exp_Amount':str(x[2])} for x in rec]
        return records
    #refresh recyclerview
    def exp_refresh_recycleview(self):
     # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('expenses').ids.exp_rv.data = self.data_from_dataset_exp()
        
     #  ---- refresh the recycleview: ---- #
        self.root.get_screen('expenses').ids.exp_rv.refresh_from_data()
#----------------------------SALES FUNCTIONS----------------
  #add customer method
    def add_sales(self,inst):
        quantity=self.sl_dialog.content_cls.ids.sl_quantity.text
        guage=self.sl_dialog.content_cls.ids.sl_gauge.text
        unitprice=self.sl_dialog.content_cls.ids.sl_unitprice.text
        colour=self.sl_dialog.content_cls.ids.sl_color.text
        
        if quantity!='' and guage!='' and unitprice!=''and colour!='':
            Database().add_sales(quantity,guage,unitprice,colour)
            toast(quantity+" of "+ guage+"mm " +" added successfully!")
            self.sl_refresh_recycleview()
            self.sl_dialog.dismiss()
        elif quantity=='' and guage!=''and unitprice!='' and colour!='':
            toast("Enter Quantity!")
        elif guage=='' and quantity!=''and unitprice!='' and colour!='':
            toast("Enter gauge!")  
        elif unitprice=='' and guage!=''and colour!='' and quantity!='':
            toast("Enter unitprice")
        elif colour=='' and guage!=''and unitprice!='' and quantity!='':
            toast("Enter unitprice")
        else:
            toast("Empty Fields!")
    #add expense dialog
    def add_sales_confirmation_dialog(self):
        if not self.sl_dialog:
            self.sl_dialog = MDDialog(
                title="ADD SALES",
                type="custom",
                content_cls=SlContents(),
                buttons=[
                    MDRectangleFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release= self.closeSlDialog
                    ),
                    MDRectangleFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.add_sales
                    ),
                ],
            )
        self.sl_dialog.open()
   
        # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('sales').ids.sl_rv.data = self.data_from_dataset_sl()
            
        #  ---- refresh the recycleview: ---- #
        self.root.get_screen('sales').ids.sl_rv.refresh_from_data()
    #data to add to recyclerview
    def data_from_dataset_sl(self):
        rec= Database().all_sales()
        # ---- format your data for recycleview here ---- #
        records=[{'sl_ID': str(x[0]),'sl_Quantity':str(x[1]),'sl_Guage':str(x[2]),'sl_UnitPrice':str(x[3]),'sl_Color':str(x[4])} for x in rec]
        return records
    #refresh recyclerview
    def sl_refresh_recycleview(self):
        # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('sales').ids.sl_rv.data = self.data_from_dataset_sl()
        
     #  ---- refresh the recycleview: ---- #
        self.root.get_screen('sales').ids.sl_rv.refresh_from_data()
        
#---------------------------END of Sales Functions-----------------------------
#--------------------Purchases Functions-----------------------------------------
    #add purchases method
    def add_purchases(self,inst):
        guage=self.p_dialog.content_cls.ids.p_gauge.text
        quantity=self.p_dialog.content_cls.ids.p_quantity.text
        unitprice=self.p_dialog.content_cls.ids.p_unitprice.text
        supplier=self.p_dialog.content_cls.ids.p_supplier.text
        
        if quantity!='' and guage!='' and unitprice!=''and supplier!='':
            Database().add_purchase(guage,quantity,unitprice,supplier)
            toast(quantity+" of "+ guage+"mm " +" added successfully!")
            self.p_refresh_recycleview()
            self.p_dialog.dismiss()
        elif quantity=='' and guage!=''and unitprice!='' and supplier!='':
            toast("Enter Quantity!")
        elif guage=='' and quantity!=''and unitprice!='' and supplier!='':
            toast("Enter gauge!")  
        elif unitprice=='' and guage!=''and supplier!='' and quantity!='':
            toast("Enter unitprice")
        elif supplier=='' and guage!=''and unitprice!='' and quantity!='':
            toast("Enter Supplier")
        else:
            toast("Empty Fields!")
    #add expense dialog
    def add_purchases_confirmation_dialog(self):
        if not self.p_dialog:
            self.p_dialog = MDDialog(
                title="ADD STOCK DETAILS",
                type="custom",
                content_cls=PContents(),
                buttons=[
                    MDRectangleFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release= self.closePDialog
                    ),
                    MDRectangleFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_release=self.add_purchases
                    ),
                ],
            )
        self.p_dialog.open()
   
        # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('purchases').ids.p_rv.data = self.data_from_dataset_p()
            
        #  ---- refresh the recycleview: ---- #
        self.root.get_screen('purchases').ids.p_rv.refresh_from_data()
    #data to add to recyclerview
    def data_from_dataset_p(self):
        rec= Database().all_purchases()
        # ---- format your data for recycleview here ---- #
        records=[{'p_ID': str(x[0]),'p_Guage':str(x[1]),'p_Quantity':str(x[2]),'p_Unitprice':str(x[3]),'p_Supplier':str(x[4])} for x in rec]
        return records
    #refresh recyclerview
    def p_refresh_recycleview(self):
        # ----- Update the recycleview data in the .kv file: ---- #
        self.root.get_screen('purchases').ids.p_rv.data = self.data_from_dataset_p()
        
     #  ---- refresh the recycleview: ---- #
        self.root.get_screen('purchases').ids.p_rv.refresh_from_data()




if __name__ == '__main__':
    Glassy().run()