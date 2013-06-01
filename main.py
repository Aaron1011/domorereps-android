try:
    from secret_settings import *
except:
    print "No additional settings file found"

import sys
from os import environ
import error_reporting
DEBUG = environ.get('DOMO_DEBUG')

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import *

engine = sqlalchemy.create_engine("sqlite:///db.sqlite3")
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(engine)

if not DEBUG:
    error_reporting.start_reporting(engine)

import kivy
kivy.require('1.7.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from screens import *

import yaml
import os
from session_decorator import *

class DomorerepsApp(App):
    def build(self):
        self.load_exercises()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ExercisesScreen(Session, name='exercises'))
        sm.add_widget(EditExerciseScreen(Session, name='editexercise'))
        sm.add_widget(WorkoutScreen(name='workout'))
        return sm

    def load_exercises(self):
        with transactional_session(Session) as session:
            version = session.query(ExerciseVersion).all()
            if not version or version[0].number < 1:
                print "Loading exercises"
                version = ExerciseVersion()
                version.number = 1
                session.add(version)
                with open('data/exercises.yml') as f:
                    data = yaml.load(f.read())

                    for exercise in data.values():
                        name = exercise['name']
                        weightless = exercise['weightless']

                        exercise = Exercise(name, weightless)
                        session.add(exercise)

if __name__ == "__main__":
    DomorerepsApp().run()
