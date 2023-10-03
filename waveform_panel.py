# import kivy module
import kivy
   
# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")
 
# Kivy Example App for the slider widget
from kivy.app import App
 
# The GridLayout arranges children in a matrix.
from kivy.uix.gridlayout import GridLayout
 
# If we will not import this module
# It will through the error
from kivy.uix.slider import Slider
 
# The Label widget is for rendering text.
from kivy.uix.label import Label
 
# Property that represents a numeric value
# within a minimum bound and / or maximum
# bound – within a numeric range.
from kivy.properties  import NumericProperty
 # import buiilder
from kivy.lang import Builder
# class in which we are defining the
# sliders and its effects

kv = """
FloatLayout:
    GridLayout:
        cols: 1
        rows: 1
        GridLayout:
            cols: 1
            rows: 2
            GridLayout:
                cols: 2
                rows: 1
                Label:
                    text: "Video position:"
        ----------------------
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
  
 
# creating the object root for ButtonApp() class 
root = SliderExample()
   
# run function runs the whole program
# i.e run() method which calls the
# target function passed to the constructor.
root.run()