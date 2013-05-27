from sqlalchemy import Column, Integer, Float, String, Date, Table, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

sessiontemplate_exercises = Table('sessiontemplate_exercises', Base.metadata,
        Column('session_template_id', Integer,
            ForeignKey('sessiontemplates.id')),
        Column('exercise_id', Integer, ForeignKey('exercises.id'))
)

class ExerciseSessionExercise(Base):
    __tablename__ = 'exercisesessionexercises'
    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    exercise_session_id = Column(Integer, ForeignKey('exercisesessions.id'))

    exercise = relationship("Exercise", backref=backref('exercise_session_exercises', order_by=id))
    exercise_session = relationship("ExerciseSession", backref=
            backref('exercise_session_exercises', order_by=id))

    exerciseName = Column(String)
    exerciseSessionStart = Column(Date)


class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    weightless = Column(Boolean)
    session_templates = relationship('SessionTemplate',
            secondary=sessiontemplate_exercises, backref='exercises')

    def __init__(self, name=None, weightless=None):
        self.name = name
        self.weightless = weightless

class ExerciseSession(Base):
    __tablename__ = 'exercisesessions'
    id = Column(Integer, primary_key=True)
   
    dateSavedToServer = Column(Date)
    start = Column(Date)
    end = Column(Date)

class ExerciseSet(Base):
    __tablename__ = 'exercisesets'
    id = Column(Integer, primary_key=True)

    date = Column(Date)
    reps = Column(Integer)
    weight = Column(Float)
    exersise_session_exercise_id = Column(Integer,
            ForeignKey('exercisesessionexercises.id'))

    exercise_session_exercise = relationship("ExerciseSessionExercise",
            backref=backref('exercise_sets', order_by=id))

class SessionTemplate(Base):
    __tablename__ = 'sessiontemplates'
    id = Column(Integer, primary_key=True)

    name = Column(String)

class PythonException(Base):
    __tablename__ = 'exceptions'
    id = Column(Integer, primary_key=True)
    data = Column(String)

class ExerciseVersion(Base):
    __tablename__ = 'exerciseversion'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
