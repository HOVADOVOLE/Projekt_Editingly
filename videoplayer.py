from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

class VideoPlayerApp(BoxLayout):
    def __init__(self):
        super().__init__()
        self.size_hint = (0.5, 0.6)
        self.pos_hint = {'right': 0.95, 'top': 0.95}
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Vytvoření černého pozadí
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Černá barva v RGBA
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.video = VideoPlayer(size_hint=(1, 1))
        self.video.bind(on_touch_down=self.on_touch_down)
        self.add_widget(self.video)

        # Propojení velikosti a pozice čtverce s velikostí a pozicí widgetu
        self.bind(pos=self.aktualizovat_ctverec, size=self.aktualizovat_ctverec)

        # Popup pro file manager
        self.popup_file_manager = None

    def aktualizovat_ctverec(self, instance, hodnota):
        # Aktualizace velikosti a pozice čtverce při změně velikosti nebo pozice widgetu
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        if self.video.collide_point(*touch.pos):
            if self.video.source == '':
                # Zdroj videa není nastaven, umožnit uživateli vybrat vlastní zdroj videa
                self.otevrit_file_manager(None)  # Předáme None jako placeholder pro 'instance'

    def otevrit_file_manager(self, instance):
        # Vytvoření a zobrazení popupu s file managerem
        file_chooser = FileChooserIconView(path='.', filters=['*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv'])
        file_chooser.bind(on_submit=self.vybrat_soubor)
        file_chooser.bind(on_cancel=self.zavrit_file_manager)
        self.popup_file_manager = Popup(title='Vyberte video', content=file_chooser, size_hint=(0.9, 0.9))
        self.popup_file_manager.open()

    def vybrat_soubor(self, instance, selection, *args):
        if selection:
            self.video.source = selection[0]
            self.video.state = 'play'  # Spustit přehrávání videa po nastavení nového zdroje
        self.popup_file_manager.dismiss()

    def zavrit_file_manager(self, instance):
        self.popup_file_manager.dismiss()