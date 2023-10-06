# import kivy module
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

kv = """
BoxLayout:
    GridLayout:
        cols: 1
        GridLayout:
            cols: 1
            rows: 2
            GridLayout:
                cols: 2
                rows: 1
                BoxLayout:
                    Label:
                        text: "Video position:"
                    
                
        #----------------------
        GridLayout:
            cols: 1
            rows: 2

            canvas:
                Color:
                    rgba: 0, 0, 1, 1  # Barva pozadí
                Rectangle:
                    size: self.width * 0.85, 250

            Slider:
                min: 0
                max: 100
                id: brightnessControl
                size_hint: None, None
                size: self.parent.width * 0.85, 50

"""


class myApp(App):
    def build(self):
        Window.maximize()
        return FloatLayout()

class WidgetContainer(GridLayout):
 
    def __init__(self, **kwargs):
        super(WidgetContainer, self).__init__(**kwargs)
        
        self.brightnessControl = Slider(min = 0, max = 100)
        self.add_widget(self.brightnessControl)
# The app class
class SliderExample(App):
    def build(self):
        #widgetContainer = WidgetContainer()
        return Builder.load_string(kv)

#root = SliderExample()
#root.run()

if __name__ == '__main__':
    myApp().run()