
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.lang import Builder
import re
# zdroj originálního kódu: https://github.com/kivy/kivy/wiki/Editable-ComboBox
Builder.load_string('''
<DDNButton@Button>
    size_hint_y: None
    height: dp(45)
''')


class ComboBox(Factory.TextInput):

    options = ListProperty(('', ))
    _options = ListProperty(('', ))
    option_cls = ObjectProperty(Factory.DDNButton)

    select = StringProperty('')


    def __init__(self, **kw):
        ddn = self.drop_down = Factory.DropDown()
        ddn.bind(on_select=self.set_select)
        super().__init__(**kw)
        self.trigger_dropdown = Clock.create_trigger(self.drop_down_triggered, 1/2)
        self.write_tab = False
        self.multiline = False

    def on_text_validate(self):
        if not self._options:
            return

        # print(self.text, self._options[-1])
        if not self.text in self._options[-1]:
            return

        self.set_select(self, self._options[-1])

    def on_options(self, instance, value):
        self._options = value

    def on__options(self, instance, value):
        ddn = self.drop_down
        ddn.clear_widgets()
        for option in value:
            widg = self.option_cls(text=option)
            widg.bind(on_release=lambda btn: ddn.select(btn.text))
            ddn.add_widget(widg)

    def set_select(self, *args):
        # print('on_select', args)
        if self.text != args[1]:
            self.select = args[1]
            self.text = args[1]
            self.drop_down.dismiss()

    def on_text(self, instance, value):
        self.trigger_dropdown()

    def drop_down_triggered(self, dt):
        value = self.text
        instance = self
        # print(f'on_text {instance} "{value}"')
        if value == '':
            instance._options = self.options
            return
        else:
            # print(f'on_text {instance} "{value}" on_else')
            if value in self.options:
                self.drop_down.pos = 0, -1000
                return

            r = re.compile(f".*{value}", re.IGNORECASE)
            match = filter(r.match, instance.options)
            #using a set to remove duplicates, if any.
            instance._options = list(set(match))
            # print(instance._options)

            instance.drop_down.dismiss()
            # print(instance.parent, instance.pos)
            Clock.schedule_once(lambda dt: instance.drop_down.open(instance), .1)

    def on_touch_up(self, touch):
        # print('focus', value, self.text)
        if touch.grab_current == self:
            self.text = ''
            self.drop_down.open(self)
        # else:
        #     self.drop_down.dismiss()

if __name__ == '__main__':
    from kivy.app import App
    class MyApp(App):
        def build(self):
            return Builder.load_string('''
FloatLayout:
    BoxLayout:
        size_hint: .5, None
        pos: 0, root.top - self.height
        ComboBox:
            options: ['Hello', 'World']
        ComboBox:
            options: '99 bottles of beer on the wall , Tito hit of them down from the wall ,  98 bottles of beer!'.split(' ')
        Button


''')
    MyApp().run()