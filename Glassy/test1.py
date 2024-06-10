#main.py
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

Builder.load_string(
'''
<ListItemWithCheckbox>:
    id: the_list_item
    markup: True

    LeftCheckbox:
        id: check
        on_release: 
            root.mark(check, the_list_item)

    IconRightWidget:
        icon: 'trash-can-outline'
        theme_text_color: "Custom"
        text_color: 1, 0, 0, 1
        on_release:
            root.delete_item(the_list_item)
MDFloatLayout:
    MDLabel:
        id: task_label
        halign: 'center'
        markup: True
        text: "[u][size=48][b]My Tasks[/b][/size][/u]"
        pos_hint: {'y': .45}

    ScrollView:
        pos_hint: {'center_y': .5, 'center_x': .5}
        size_hint: .9, .8

        MDList:
            id: container

    MDFloatingActionButton:
        icon: 'plus-thick'
        on_release: app.show_task_dialog() #functionality to be added later
        elevation_normal: 12
        pos_hint: {'x': .8, 'y':.05}
<DialogContent>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint: 1, None
    height: "130dp"

    GridLayout:
        rows: 1

        MDTextField:
            id: task_text
            hint_text: "Add Task..."
            pos_hint: {"center_y": .4}
            max_text_length: 50
            on_text_validate: (app.add_task(task_text, date_text.text), app.close_dialog())

        MDIconButton:
            icon: 'calendar'
            on_release: root.show_date_picker()
            padding: '10dp'

    MDLabel:
        spacing: '10dp'
        id: date_text

    BoxLayout:
        orientation: 'horizontal'

        MDRaisedButton:
            text: "SAVE"
            on_release: (app.add_task(task_text, date_text.text), app.close_dialog())
        MDFlatButton:
            text: 'CANCEL'
            on_release: app.close_dialog()

'''
)
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk


    def mark(self, check, the_list_item):
        '''mark the task as complete or incomplete'''
        if check.active == True:
            # add strikethrough to the text if the checkbox is active
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
        else:
            # we shall add code to remove the strikethrough later
            pass

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)



class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''
class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when useer first opens dialog box
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))


    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

class MainApp(MDApp):
    task_list_dialog = None # Here
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "DeepPurple"

    # Add the below functions
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        '''Add task to the list of tasks'''

        print(task.text, task_date)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(text='[b]'+task.text+'[/b]', secondary_text=task_date))
        task.text = '' # set the dialog entry to an empty string(clear the text entry)
if __name__ == '__main__':
    app = MainApp()
    app.run()