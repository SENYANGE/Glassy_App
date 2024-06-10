
from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from database import Database

kv = """
<Row@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: ''
    TextInput:
        multiline: False
        text: root.value
        on_text_validate: root.update(args[0].text)
       
<Test>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 1
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Populate with text'
            on_press: root.populate_with_text()
        Button:
            text: 'Populate with same text'
            on_press: root.populate_with_same_text()
        Button:
            text: 'Populate with blanks'
            on_press: root.populate_with_blanks()
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: 'Row'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
"""


class Row(RecycleDataViewBehavior, BoxLayout):
    def update(self, text):
        self.parent.parent.data[self.index]['value'] = text
        self.parent.parent.refresh_from_data()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(Row, self).refresh_view_attrs(rv, index, data)


class Test(BoxLayout):
    db=Database()

    def populate_with_text(self):
        records=self.db.all_customers()
        if records!=[]:
            self.rv.data = [{'value':str(x[2]), 'index': str(x[0])}
                            for x in records]
            self.rv.refresh_from_data()

    def populate_with_same_text(self):
        self.rv.data = [{'value': 'None', 'index': x}
                        for x in range(50)]
        self.rv.refresh_from_data()

    def populate_with_blanks(self):
        self.rv.data = [{'value': '', 'index': x}
                        for x in range(50)]
        self.rv.refresh_from_data()


Builder.load_string(kv)


class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()