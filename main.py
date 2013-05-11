import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    pass

class ExercisesScreen(Screen):
    pass

class DomorerepsApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ExercisesScreen(name='exercises'))
        self.load_exercises()
        return sm

if __name__ == "__main__":
    DomorerepsApp().run()
