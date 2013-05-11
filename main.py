import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

import yaml
import sqlite3

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

    def load_exercises(self):
        with open('data/exercises.yml') as f:
            data = yaml.load(f.read())
            conn = sqlite3.connect('db.sqlite3')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS exercises (name text, \
            weightless integer, unique (name))''')

            for exercise in data.values():
                name = exercise['name']
                weightless = exercise['weightless']
                c.execute('''INSERT OR IGNORE INTO exercises VALUES (?, ?)''',
                        (name, weightless))
            conn.commit()
        conn.close()

if __name__ == "__main__":
    DomorerepsApp().run()
