from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, DictProperty
from kivy.clock import Clock
from kivy.core.window import Window
from models import *
from session_decorator import *

from sqlalchemy.orm.exc import MultipleResultsFound

from types import MethodType

class HomeScreen(Screen):
    def workout_options(self):
        layout = BoxLayout(orientation='vertical')

        blank_btn = Button(text='Start Blank', size_hint=[.8, 1],
                pos_hint={'x': .1}, on_release=self.new_workout)
        template_btn = Button(text='Start from Template', size_hint=[.8, 1],
                pos_hint={'x': .1})
        previous_btn = Button(text='Copy from Previous', size_hint=[.8, 1],
                pos_hint={'x': .1})

        layout.add_widget(blank_btn)
        layout.add_widget(template_btn)
        layout.add_widget(previous_btn)

        self.popup = ModalView(content=layout, size_hint=[1, .5],
                pos_hint={'top': .5})
        self.popup.add_widget(layout)

        self.popup.open()

    def new_workout(self, instance):
        self.popup.dismiss()
        self.manager.current = 'workout'


class ExercisesScreen(Screen):
    layout = ObjectProperty(None)
    add_exercise = ObjectProperty(None)
    scroll_height = NumericProperty(0)

    def __init__(self, session, **kwargs):
        super(ExercisesScreen, self).__init__(**kwargs)
        self.session_class = session
        self.add_exercise.bind(on_press=self.new_exercise)

    def on_pre_enter(self):
        self.layout.clear_widgets()
        self.scroll_height = 0
        for exercise in self.fetch_exercises():
            button = Button(text=exercise.name, size_hint=(.8, None),
                    pos_hint={'x': .1}, height=Window.height / 12)
            button.weightless = exercise.weightless
            button.bind(on_press=self.change_screen)
            self.scroll_height += button.height
            self.layout.add_widget(button)


    def fetch_exercises(self):
        with transactional_session(self.session_class) as session:
            return session.query(Exercise).all()

    def new_exercise(self, instance):
        edit_screen = self.manager.get_screen('editexercise')
        exercise = Exercise()
        exercise.name = ''

        edit_screen.exercise = exercise
        edit_screen.name_input.text = exercise.name
        self.manager.current = 'editexercise'

    def get_exercise(self, name):
        with transactional_session(self.session_class) as session:
            return session.query(Exercise).filter(Exercise.name==name).one()


    def change_screen(self, instance):
        edit_screen = self.manager.get_screen('editexercise')

        with transactional_session(self.session_class) as session:
            exercise = session.query(Exercise).filter(Exercise.name==instance.text).one()

        edit_screen.exercise = exercise
        edit_screen.name_input.text = exercise.name
        if exercise.weightless and edit_screen.weightless_button.state == 'normal':
            edit_screen.weightless_button.trigger_action()
        elif not exercise.weightless and edit_screen.weights_button.state == 'normal':
            edit_screen.weights_button.trigger_action()

        self.manager.current = 'editexercise'
         

def trigger_action(self, duration=0.1):
    '''Trigger whatever action(s) have been bound to the button by calling
    both the on_press and on_release callbacks.

    This simulates a quick button press without using any touch events.

    Duration is the length of the press in seconds. Pass 0 if you want
    the action to happen instantly.

    .. versionadded:: 1.8.0
    '''
    self._do_press()
    self.dispatch("on_press")
    def trigger_release(dt):
        self._do_release()
        self.dispatch("on_release")
    if not duration:
        trigger_release(0)
    else:
        Clock.schedule_once(trigger_release, duration)

class EditExerciseScreen(Screen):
    layout = ObjectProperty(None)
    exercise = ObjectProperty(None)
    name_input = ObjectProperty(None)
    weightless_button = ObjectProperty(None)
    weights_button = ObjectProperty(None)

    def __init__(self, session, **kwargs):
        super(EditExerciseScreen, self).__init__(**kwargs)
        self.session_class = session
        self.weightless_button.trigger_action = MethodType(trigger_action,
                self.weightless_button, ToggleButton)

        self.weights_button.trigger_action = MethodType(trigger_action,
                self.weights_button, ToggleButton)

    def save(self):
        with transactional_session(self.session_class) as session:
            session.add(self.exercise)

        popup = Popup(title='', content=Label(text='Exercise Saved!'),
                size_hint=(.5, .5))

        popup.open()

    def delete_exercise(self):
        with transactional_session(self.session_class) as session:
           session.delete(self.exercise)
        self.manager.current = 'exercises'

class WorkoutScreen(Screen):
    layout = ObjectProperty(None)
    scroll_height = NumericProperty(0)
    exercises = DictProperty()

    def add_exercise(self, exercise):
        if not exercise in self.exercises:
            self.exercises[exercise] = []

    def on_pre_enter(self):
        self.layout.clear_widgets()
        self.scroll_height = 0
        for exercise in self.exercises:
            label = Label(text=exercise.name)
            self.scroll_height += label.height
            self.layout.add_widget(label)

            layout = StackLayout()
            for workout in self.exercises[exercise]:
                self.scroll_height += workout.height
                layout.add_widget(workout)


class SelectExerciseScreen(ExercisesScreen):

    def change_screen(self, instance):
        workout_screen = self.manager.get_screen('workout')
        exercise = self.get_exercise(instance.text)

        workout_screen.add_exercise(exercise)
        self.manager.current = 'workout'
