import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

import yaml
import sqlalchemy
from models import * 
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine("sqlite:///db.sqlite3")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine) 


class HomeScreen(Screen):
    pass

class ExercisesScreen(Screen):
    layout = ObjectProperty(None)

    def fetch_exercises(self):
       session = Session()
       return session.query(Exercise).all()

    def on_press(self, instance):
        print instance.weightless

    def __init__(self, **kwargs):
        super(ExercisesScreen, self).__init__(**kwargs)
        for exercise in self.fetch_exercises():
            button = Button(text=exercise.name, size_hint=(.8, .1),
                    pos_hint={'x': .1})
            button.weightless = exercise.weightless
            button.bind(on_press=self.on_press)
            self.layout.add_widget(button)

class DomorerepsApp(App):
    def build(self):
        self.load_exercises()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ExercisesScreen(name='exercises'))
        return sm

    def load_exercises(self):
        session = Session()
        with open('data/exercises.yml') as f:
            data = yaml.load(f.read())

            for exercise in data.values():
                name = exercise['name']
                weightless = exercise['weightless']

                exercise = Exercise(name, weightless)
                session.add(exercise)
            session.commit()

if __name__ == "__main__":
    DomorerepsApp().run()
