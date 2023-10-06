import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

class myApp(App):
    def build(self):
        Window.maximize()
        return Builder.load_file('my.kv')

    def move_slider_backward(self):
        if self.root.ids.brightnessControl.value > self.root.ids.brightnessControl.min:
            self.root.ids.brightnessControl.value -= 0.05 * (self.root.ids.brightnessControl.max - self.root.ids.brightnessControl.min)

    def move_slider_forward(self):
        if self.root.ids.brightnessControl.value < self.root.ids.brightnessControl.max:
            self.root.ids.brightnessControl.value += 0.05 * (self.root.ids.brightnessControl.max - self.root.ids.brightnessControl.min)


if __name__ == '__main__':
    myApp().run()