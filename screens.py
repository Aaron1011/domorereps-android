from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from models import *

class HomeScreen(Screen):
    pass

class ExercisesScreen(Screen):
    layout = ObjectProperty(None)

    def __init__(self, session, **kwargs):
        super(ExercisesScreen, self).__init__(**kwargs)
        self.session_class = session
        self.session = session()

    def on_pre_enter(self):
        self.layout.clear_widgets()
        for exercise in self.fetch_exercises():
            button = Button(text=exercise.name, size_hint=(.8, .1),
                    pos_hint={'x': .1})
            button.weightless = exercise.weightless
            button.bind(on_press=self.change_screen)
            self.layout.add_widget(button)


    def fetch_exercises(self):
       return self.session.query(Exercise).all()

    def change_screen(self, instance):
        edit_screen = self.manager.get_screen('editexercise')

        query = self.session.query(Exercise).filter(Exercise.name==instance.text)
        exercise = query.one()

        edit_screen.exercise = exercise
        edit_screen.name_input.text = exercise.name
        self.manager.current = 'editexercise'
         

class EditExerciseScreen(Screen):
    layout = ObjectProperty(None)
    exercise = ObjectProperty(None)
    name_input = ObjectProperty(None)

    def __init__(self, session, **kwargs):
        super(EditExerciseScreen, self).__init__(**kwargs)
        self.session_class = session
        self.session = session()

    def save(self):
        self.session.commit()
        popup = Popup(title='', content=Label(text='Exercise Saved!'),
                size_hint=(.5, .5))

        popup.open()
