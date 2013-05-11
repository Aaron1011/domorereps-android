import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class HomeScreen(BoxLayout):
    pass


class DomorerepsApp(App):
    def build(self):
        return HomeScreen()

if __name__ == "__main__":
    DomorerepsApp().run()
