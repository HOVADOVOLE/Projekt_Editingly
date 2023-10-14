from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color

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

        video = VideoPlayer(size_hint=(1, 1))
        video.bind(on_touch_down=self.on_touch_down)
        self.add_widget(video)

        # Propojení velikosti a pozice čtverce s velikostí a pozicí widgetu
        self.bind(pos=self.aktualizovat_ctverec, size=self.aktualizovat_ctverec)

    def aktualizovat_ctverec(self, instance, hodnota):
        # Aktualizace velikosti a pozice čtverce při změně velikosti nebo pozice widgetu
        self.rect.pos = self.pos
        self.rect.size = self.size
    def on_touch_down(self, instance):
        if instance.source == '':
            instance.source = 'video.mp4'