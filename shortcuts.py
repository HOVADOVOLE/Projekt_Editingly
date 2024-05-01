import keyboard
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from threading import Thread
from functools import partial

# Dictionary to store shortcuts and their corresponding actions
shortcuts = {
    "ctrl+g": "generate_subtitles",
    "ctrl+w": "toggle_sidepanel",
    "ctrl+s": "save_changes",
    "ctrl+del": "close_application",
    "ctrl+o": "open_file",
    "ctrl+n": "new_project",
    "ctrl+shift+s": "save_as"
}

# Function to be called when the shortcut is triggered
def action(shortcut):
    print("Shortcut", shortcut, "triggered. Performing", shortcuts[shortcut])
    if shortcuts[shortcut] == "generate_subtitles":
        generate_subtitles()
    elif shortcuts[shortcut] == "toggle_sidepanel":
        toggle_sidepanel()
    elif shortcuts[shortcut] == "save_changes":
        save_changes()
    elif shortcuts[shortcut] == "close_application":
        close_application()
    elif shortcuts[shortcut] == "open_file":
        open_file()
    elif shortcuts[shortcut] == "new_project":
        new_project()
    elif shortcuts[shortcut] == "save_as":
        save_as()

# Register all the shortcuts
for shortcut in shortcuts:
    keyboard.add_hotkey(shortcut, action, args=(shortcut,))

# Function to change a shortcut
def change_shortcut(old_shortcut):
    new_shortcut = input("Enter the new shortcut: ")
    if new_shortcut not in shortcuts:
        shortcuts[new_shortcut] = shortcuts.pop(old_shortcut)
        keyboard.remove_hotkey(old_shortcut)
        keyboard.add_hotkey(new_shortcut, action, args=(new_shortcut,))
        print("Shortcut", old_shortcut, "changed to", new_shortcut)
    else:
        print("Shortcut already exists")

# Shortcut for generating subtitles
def generate_subtitles():
    pass

# Shortcut for toggling the side panel
def toggle_sidepanel():
    # Close the side panel
    pass

# Shortcut for saving changes
def save_changes():
    # Save changes
    pass

# Shortcut for closing the application
def close_application():
    pass

# Shortcut for opening a project
def open_file():
    print("Opening file")

# Shortcut for creating a new project
def new_project():
    print("Creating new project")

# Shortcut for saving a project as
def save_as():
    print("Saving as")

class ShortcutsApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        grid = GridLayout(cols=2)
        for key, value in shortcuts.items():
            label = Label(text=f"{key} - {value}")
            change_button = Button(text="Change Shortcut")
            change_button.bind(on_press=partial(self.show_popup, key))
            grid.add_widget(label)
            grid.add_widget(change_button)
        layout.add_widget(grid)
        return layout

    def show_popup(self, key, *args):
        content = BoxLayout(orientation='vertical')
        self.popup = Popup(title='Change Shortcut', content=content, size_hint=(None, None), size=(400, 200))
        self.current_key = key

        label = Label(text=f"Current Shortcut: {key}")
        content.add_widget(label)

        input_label = Label(text="Press new shortcut:")
        content.add_widget(input_label)

        input_field = TextInput()
        content.add_widget(input_field)

        input_thread = Thread(target=self.get_key, args=(input_field,))
        input_thread.start()

        content.add_widget(Button(text='Close', on_press=self.popup.dismiss))
        self.popup.open()

    def get_key(self, input_field):
        def on_press(event):
            if event.event_type == 'down':
                Clock.schedule_once(lambda dt: self.update_text_input(input_field, event.name))
                if event.name == 'enter':
                    self.save_new_shortcut(input_field.text)
                    self.popup.dismiss()

        keyboard.hook(on_press)

    def update_text_input(self, input_field, text):
        current_text = input_field.text
        if current_text:
            current_text += " + "
        input_field.text = current_text + text

    def save_new_shortcut(self, new_shortcut):
        key = self.current_key
        if new_shortcut not in shortcuts:
            shortcuts[new_shortcut] = shortcuts.pop(key)
            keyboard.remove_hotkey(key)
            keyboard.add_hotkey(new_shortcut, action, args=(new_shortcut,))
            print("Shortcut", key, "changed to", new_shortcut)
        else:
            print("Shortcut already exists")

if __name__ == '__main__':
    ShortcutsApp().run()
