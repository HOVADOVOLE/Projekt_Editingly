from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from title_manager import title_manager
from subtitle_handler import Subtitle_Handler
from kivy.uix.popup import Popup

class InteractiveTable(RelativeLayout):
    def __init__(self, **kwargs):
        super(InteractiveTable, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (0.75, 1)
        self.pos_hint = {'top': 0.95, 'left': 0.90}

        self.subtitle_handler = Subtitle_Handler()

        self.row_num = 0
        self.title_manager = title_manager()
        self.data_table = None


        # Vykreslení tabulky a boxu pro úpravué
        self.render_table()
        self.render_modify_box()

        # Přidání MDDataTable do RelativeLayout
        self.add_widget(self.data_table)
        self.add_widget(self.modify_box)

        Clock.schedule_interval(self.clock_action_handler, 0.2)
    def update_values(self, *args):
        # TODO zkusit přecastování na float a popřípadě zaokrouhlit
        if self.is_float(self.start_input.text) and self.is_float(self.end_input.text):
            if float(self.start_input.text) < float(self.end_input.text):
                self.data_table.row_data[self.row_num] = (str(self.row_num+1), self.start_input.text, self.end_input.text, self.text_input.text)
                self.subtitle_handler.modify_subtitle(self.row_num, self.start_input.text, self.end_input.text, self.text_input.text)
            else:
                # start je větší než end
                pass
        else:
            # nejsou float
            pass
    def is_float(self, value):
        if value is not None:
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False
    def delete_row(self, *args):
        try:
            self.data_table.row_data.pop(self.row_num)
            self.title_manager.remove_section(self.row_num)
            self.subtitle_handler.remove_subtitle(self.row_num) # TODO - zkotntolovat jestli není o index napřed
        except:
            return
    def render_table(self):
        # Inicializace MDDataTable s novým řádkem
        self.data_table = MDDataTable(
            rows_num=1000,
            size_hint=(0.55, 0.5),
            pos_hint={'left': 0.7, 'top': 0.99},
            column_data=[
                ('#', dp(9)),
                ('Start Time', dp(18)),
                ('End Time', dp(18)),
                ('Text', dp(65)),
            ],
        )
        self.data_table.bind(on_row_press=self.select_row)
    def select_row(self, table, row):
        self.row_num = int(row.index/len(table.column_data))
        self.start_input.text = str(self.data_table.row_data[self.row_num][1])
        self.end_input.text = str(self.data_table.row_data[self.row_num][2])
        self.text_input.text = str(self.data_table.row_data[self.row_num][3])
    def render_modify_box(self):
        self.modify_box = BoxLayout(orientation='horizontal', size_hint=(0.55, 0.1), pos_hint={'left': 0.7, 'top': 0.48})
        self.button_box = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.start_input = TextInput(hint_text='Start Time', multiline=False, size_hint_y=0.4, pos_hint={'center_y': 0.5})
        self.end_input = TextInput(hint_text='End Time', multiline=False, size_hint_y=0.4, pos_hint={'center_y': 0.5})
        self.text_input = TextInput(hint_text='Text', multiline=False, size_hint_y=0.4, pos_hint={'center_y': 0.5})

        self.modify_box.add_widget(self.start_input)
        self.modify_box.add_widget(self.end_input)
        self.modify_box.add_widget(self.text_input)

        modify = Button(text='Modify')
        modify.bind(on_release=self.update_values)

        delete = Button(text='Delete')
        delete.bind(on_release=self.delete_row)

        self.button_box.add_widget(modify)
        self.button_box.add_widget(delete)
        self.modify_box.add_widget(self.button_box)
    def add_row(self, start, end, text) -> None:
        self.data_table.add_row((str(len(self.data_table.row_data)+1), start, end, "text"))
        start = round(start, 2)
        end = round(end, 2)
        self.subtitle_handler.add_subtitle(start, end, text)

        self.title_manager.add_row = False
    def remove_row(self, row_num):
        try:
            self.data_table.row_data.pop(row_num)
            #self.title_manager.remove_row = False
        except:
            return
    def clock_action_handler(self, *args):
        self.check_update_table()
        self.check_delete_row()
    def check_update_table(self):
        if self.title_manager.get_add_row():
            self.title_manager.start_time = round(self.title_manager.start_time, 2)
            self.title_manager.end_time = round(self.title_manager.end_time, 2)
            #self.subtitle_handler.add_subtitle(self.title_manager.start_time, self.title_manager.end_time, self.title_manager.text)
            self.add_row(self.title_manager.start_time, self.title_manager.end_time, self.title_manager.text)
    def check_delete_row(self):
        if self.title_manager.get_remove_row():
            self.remove_row(self.title_manager.index_to_remove)
            self.title_manager.remove_row_statement = False
            self.title_manager.index_to_remove = None