from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from kivy.uix.relativelayout import RelativeLayout

class InteractiveTable(RelativeLayout):
    def __init__(self, **kwargs):
        super(InteractiveTable, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.75, 1)
        self.pos_hint = {'top': 0.95, 'left': 1}
        # Vytvoření hlavního layoutu
        layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # Vytvoření layoutu pro tabulku s popisky sloupců
        table_layout = GridLayout(cols=4, size_hint=(0.5, 0.7), pos_hint={'top': 0.7, 'left': 1})
        header_labels = ['#', 'Start time', 'End time', 'Text']
        for label_text in header_labels:
            if label_text == '#':
                header_label = Label(text=label_text, size_hint=(0.1, None), height=40)
                table_layout.add_widget(header_label)
            else:
                header_label = Label(text=label_text, size_hint=(0.3, None), height=40)
                table_layout.add_widget(header_label)
        # Vytvoření tabulky
        for i in range(1, 11):  # 6 řádků
            table_layout.add_widget(Label(text=str(i), size_hint=(0.1, None), height=40))  # Číslo řádku
            for j in range(3):  # 3 sloupce s daty (bez čísla řádku)
                text_input = TextInput(multiline=False, size_hint=(0.3, None), height=40)
                table_layout.add_widget(text_input)

        layout.add_widget(table_layout)
        self.add_widget(layout)