import kivy
from kivy.app import App
from kivy.lang import Builder
import kivy_garden.contextmenu

kv = """
FloatLayout:
    id: layout
    AppMenu:
        id: app_menu
        top: root.height
        cancel_handler_widget: layout

        AppMenuTextItem:
            text: "File"
            ContextMenu:
                ContextMenuTextItem:
                    text: "New"
                ContextMenuTextItem:
                    text: "Open"
                ContextMenuTextItem:
                    text: "Save"
                ContextMenuTextItem:
                    text: "Save as..."
                ContextMenuDivider:
                ContextMenuTextItem:
                    text: "Exit"
                    on_release: app.stop()
        AppMenuTextItem:
            text: "Edit"
            ContextMenu:
                ContextMenuTextItem:
                    text: "Undo"
                ContextMenuTextItem:
                    text: "Redo"
                ContextMenuDivider:
                ContextMenuTextItem:
                    text: "Copy"
                ContextMenuTextItem:
                    text: "Cut"
                ContextMenuTextItem:
                    text: "Select all"
        AppMenuTextItem:
            text: "Tools"
            ContextMenu:
                ContextMenuTextItem:
                    text: "Split subtitle..."
                ContextMenuTextItem:
                    text: "Join subtitles..."
                ContextMenuTextItem:
                    text: "Append subtitles..."
        AppMenuTextItem:
            text: "Options"
            ContextMenu:
                ContextMenuTextItem:
                    text: "Settings..."
                ContextMenuTextItem:
                    text: "Choose language... [English]"
        AppMenuTextItem:
            text: "Help"
            ContextMenu:
                ContextMenuTextItem:
                    text: "Check for updates..."
                ContextMenuDivider:
                ContextMenuTextItem:
                    text: "Help"
                ContextMenuTextItem:
                    text: "About"
"""

class MyApp(App):
    def build(self):
        self.title = 'Editingly - 0.0.1'
        return Builder.load_string(kv)

if __name__ == '__main__':
    MyApp().run()