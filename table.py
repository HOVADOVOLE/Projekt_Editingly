from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class InteractiveTable(RelativeLayout):
    def __init__(self, **kwargs):
        super(InteractiveTable, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (0.75, 1)
        self.pos_hint = {'top': 0.95, 'left': 0.90}

        # Vykreslení tabulky a boxu pro úpravu
        self.render_table()
        self.render_modify_box()

        # Přidání MDDataTable do RelativeLayout
        self.add_widget(self.data_table)
        self.add_widget(self.modify_box)
    def update_values(self, *args):
        print('Update values')
    def delete_row(self, *args):
        print('Delete row')
    def render_table(self):
        # Inicializace MDDataTable s novým řádkem
        self.data_table = MDDataTable(
            size_hint=(0.55, 0.5),
            pos_hint={'left': 0.7, 'top': 0.99},
            column_data=[
                ('#', dp(9)),
                ('Start Time', dp(18)),
                ('End Time', dp(18)),
                ('Duration', dp(18)),
                ('Text', dp(50)),
            ],
            row_data=[
                ('1', '00:00:00', '00:00:00', '00:00:00', 'Neco text ahoj jak se máš nevím potřebuju dlouhý text lol'),
                ('2', '00:00:00', '00:00:00', '00:00:00', 'Text'),
                ('3', '00:00:00', '00:00:00', '00:00:00', 'Text'),
                ('4', '00:00:00', '00:00:00', '00:00:00', 'Text'),
                ('5', '00:00:00', '00:00:00', '00:00:00', 'Text'),
            ]
        )
    def render_modify_box(self):
        self.modify_box = BoxLayout(orientation='horizontal', size_hint=(0.55, 0.1),
                                    pos_hint={'left': 0.7, 'top': 0.48})
        self.button_box = BoxLayout(orientation='vertical', size_hint=(1, 1))

        self.modify_box.add_widget(
            TextInput(hint_text='Start Time', multiline=False, size_hint_y=0.4, pos_hint={'center_y': 0.5}))
        self.modify_box.add_widget(
            TextInput(hint_text='End Time', multiline=False, size_hint_y=0.4, pos_hint={'center_y': 0.5}))
        self.modify_box.add_widget(
            TextInput(hint_text='Text', multiline=False, size_hint_y=0.4, pos_hint={'center_y': 0.5}))
        modify = Button(text='Modify')
        modify.bind(on_release=self.update_values)
        delete = Button(text='Delete')
        delete.bind(on_release=self.delete_row)
        self.button_box.add_widget(modify)
        self.button_box.add_widget(delete)
        self.modify_box.add_widget(self.button_box)