from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class InteractiveTableApp(App):
    def build(self):
        # Vytvoření hlavního layoutu
        layout = BoxLayout(orientation='vertical')

        # Vytvoření layoutu pro tabulku s popisky sloupců
        table_layout = GridLayout(cols=4, size_hint=(0.5, 0.7), pos_hint={'top': 0.7, 'left': 1})
        header_labels = ['#', 'Start time', 'End time', 'Text']
        for label_text in header_labels:
            header_label = Label(text=label_text, size_hint=(None, None), height=40)
            table_layout.add_widget(header_label)


        rowGrid = GridLayout(cols=4, size_hint=(0.5, 0.7), pos_hint={'top': 0.7, 'left': 1})
        # Vytvoření tabulky
        for i in range(1, 7):  # 6 řádků
            rowGrid.add_widget(Label(text=str(i), size_hint=(None, None), height=40))  # Číslo řádku
            for j in range(3):  # 3 sloupce s daty (bez čísla řádku)
                text_input = TextInput(multiline=False, size_hint=(None, None), height=40)
                rowGrid.add_widget(text_input)
        table_layout.add_widget(rowGrid)
        layout.add_widget(table_layout)
        return layout

if __name__ == '__main__':
    InteractiveTableApp().run()
