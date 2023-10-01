import kivy
from kivy.app import App
from kivy.lang import Builder
import kivy_garden.contextmenu

kv = """
FloatLayout:
    id: layout
    GridLayout:
        cols: 5
        rows: 2
        spacing: 0

        Button:
            size_hint: None, None
            size: 60, 40
            text: "File"
            on_release:
                context_menu.pos = (self.x + self.width, self.y)
                context_menu.show()

        ContextMenu:
            row: 1
            column: 0
            id: context_menu
            visible: False
            cancel_handler_widget: layout

            ContextMenuTextItem:
                text: "Open"
            ContextMenuTextItem:
                text: "Save"
            ContextMenuTextItem:
                text: "Save as"
            ContextMenuTextItem:
                text: "Exit"
                on_release: app.stop()

        Button:
            size_hint: None, None
            size: 60, 40
            text: "Edit"
            on_release:
                context_menu2.pos = (self.x + self.width, self.y)
                context_menu2.show()

        ContextMenu:
            row: 1
            column: 1
            id: context_menu2
            visible: False
            cancel_handler_widget: layout

            ContextMenuTextItem:
                text: "Undo"
            ContextMenuTextItem:
                text: "Redo"
            ContextMenuTextItem:
                text: "Copy"
            ContextMenuTextItem:
                text: "Cut"
            ContextMenuTextItem:
                text: "Select all"

        Button:
            size_hint: None, None
            size: 60, 40
            text: "Tools"
            on_release:
                context_menu3.pos = (self.x + self.width, self.y)
                context_menu3.show()

        ContextMenu:
            id: context_menu3
            visible: False
            cancel_handler_widget: layout

            ContextMenuTextItem:
                text: "Split subtitle..."
            ContextMenuTextItem:
                text: "Join subtitles..."
            ContextMenuTextItem:
                text: "Append subtitles..."

        Button:
            size_hint: None, None
            size: 60, 40
            text: "Options"
            on_release:
                context_menu4.pos = (self.x + self.width, self.y)
                context_menu4.show()

        ContextMenu:
            id: context_menu4
            visible: False
            cancel_handler_widget: layout

            ContextMenuTextItem:
                text: "Settings..."
            ContextMenuTextItem:
                text: "Change language...[English]"

        Button:
            size_hint: None, None
            size: 60, 40
            text: "Help"
            on_release:
                context_menu5.pos = (self.x + self.width, self.y)
                context_menu5.show()

        ContextMenu:
            id: context_menu5
            visible: False
            cancel_handler_widget: layout

            ContextMenuTextItem:
                text: "About"
            ContextMenuTextItem:
                text: "Check for updates..."
            ContextMenuTextItem:
                text: "Help"
"""

class MyApp(App):
    def build(self):
        self.title = 'Simple context menu example'
        return Builder.load_string(kv)

if __name__ == '__main__':
    MyApp().run()