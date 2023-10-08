from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class InteractiveTableApp(App):
    def build(self):
        # Vytvoření hlavního layoutu
        layout = BoxLayout(orientation='vertical')

        # Nadpis tabulky s popisky sloupců
        header_layout = BoxLayout(size_hint=(1, 0.1))
        header_labels = ['#', 'Start time', 'End time', 'Duration', 'Text']
        for label_text in header_labels:
            header_label = Label(text=label_text, size_hint=(0.2, 1))
            header_layout.add_widget(header_label)
        layout.add_widget(header_layout)

        # Vytvoření tabulky
        for i in range(6):  # 6 řádků
            row_layout = BoxLayout(size_hint=(1, 0.1))
            row_layout.add_widget(Label(text=str(i+1), size_hint=(0.2, 1)))  # Číslo řádku
            for j in range(4):  # 4 sloupce s daty
                text_input = TextInput(multiline=False, size_hint=(0.2, 1))
                row_layout.add_widget(text_input)
            layout.add_widget(row_layout)

        return layout

if __name__ == '__main__':
    InteractiveTableApp().run()
