from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from database import Database
from kivymd.uix.button import MDFlatButton,MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast

Builder.load_string('''
<CustomerTable>:
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    customer_id:""
    customer_name: ""
    contact: ""
    orientation: "horizontal"
    Label:
        text:root.customer_id
        font_size:self.font_size
        size: self.size
    Label:
        text: root.customer_name
        size: self.size
        font_size:self.font_size
    Label:
        text: root.contact
        font_size:self.font_size
        size: self.size
    MDRectangleFlatButton:
        text:'UPDATE'
        id:cust_update
        font_size:self.font_size
        size: self.size
    MDRectangleFlatButton:
        text:'DELETE'
        id:cust_delete
        font_size:self.font_size
        size: self.size
        on_press:app.delete_customer_row()
<RV>:
    viewclass: 'CustomerTable'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,RecycleBoxLayout):
    pass

class CustomerTable(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    dialog = None
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(CustomerTable, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(CustomerTable, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
    def logout_method(self, inst):
        self.dialog.dismiss()

    def closeDialog(self, inst):
        self.dialog.dismiss() 
    def logout_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="LogOut",
                type="custom",
        
                buttons=[
                    MDRectangleFlatButton(
                        text="CANCEL",on_release= self.closeDialog
                    ),
                    MDRectangleFlatButton(
                        text="OK",on_release=self.logout_method
                    ),
                ],
            )
        self.dialog.open()
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            #self.logout_confirmation_dialog()
            toast(rv.data[index])
        else:
            print("selection removed for {0}".format(rv.data[index]))
    #delete customer row
    def delete_customer_row(self,rv,index):
        try:
            Database().delete_customer(rv.data['customer_id'])
        except Exception as e:
            print(e)
            pass
    

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        try:
            records=Database().all_customers()
            if records!=[]:
                self.data = [{"customer_id":str(x[0]),"customer_name": str(x[1]), "contact":x[2],'on_release':self.butt} for x in records]

                
            
        except Exception as e:
            print(e)
            pass  
    def butt(self, x):
        toast('button pressed')
        

class TestApp(MDApp):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()