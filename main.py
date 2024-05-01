import keyboard

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
def change_shortcut():
    print("Current shortcuts:")
    for key, value in shortcuts.items():
        print(key, "->", value)
    old_shortcut = input("Enter the shortcut to change: ")
    if old_shortcut in shortcuts:
        new_shortcut = input("Enter the new shortcut: ")
        shortcuts[new_shortcut] = shortcuts.pop(old_shortcut)
        keyboard.remove_hotkey(old_shortcut)
        keyboard.add_hotkey(new_shortcut, action, args=(new_shortcut,))
        print("Shortcut", old_shortcut, "changed to", new_shortcut)
    else:
        print("Shortcut not found")


# Zkratka pro generaci titulků
def generate_subtitles():
    pass
# Zkratka pro zavření/zobrazení sidepanelu
def toggle_sidepanel():
    # Close the sidepanel
    pass
# Zkratka pro uložení změn
def save_changes():
    # Save changes
    pass
# Zkratka pro zavření aplikace
def close_application():
    pass
# Zkratka pro otevření projektu
def open_file():
    print("Opening file")

# Zkratka pro vytvoření nového projektu
def new_project():
    print("Creating new project")
# Zkratka pro uložení projektu jako
def save_as():
    print("Saving as")

if __name__ == '__main__':
    # Start the Kivy application
    keyboard.wait("esc")