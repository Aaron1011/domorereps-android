import threading
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from models import *
import pickle
import sys
import raven
from kivy.clock import Clock
import traceback
import logging
from session_decorator import *

client = raven.Client()

error_logger = logging.getLogger('sentry.errors')
error_logger.addHandler(logging.StreamHandler())
error_logger.setLevel(logging.INFO)

class ErrorReporter(threading.Thread):

    def __init__(self, session):
        threading.Thread.__init__(self)
        self.session_class = session

    def send_report(self, data):
        client.send(**data)
        return not client.state.did_fail()

    def process_exception(self, exception):
        data = pickle.loads(exception.data)
        while not self.send_report(data):
            pass
        with transactional_session(self.session_class) as session:
            session.delete(exception)

    def run(self):

        #def insert_listener(mapper, connection, exception):
        #    self.process_exception(exception)

        #event.listen(PythonException, "after_insert", insert_listener)

        def process(dt):
            with transactional_session(self.session_class) as session:
                for exception in session.query(PythonException).all():
                    self.process_exception(exception)
        Clock.schedule_interval(process, 10)

def start_reporting(engine):
    Session = sessionmaker(bind=engine)

    reporter = ErrorReporter(Session)
    reporter.daemon = True
    reporter.start()

    def excepthook(*data):
        print "An error occured!"
        traceback.print_exception(*data)
        exception = PythonException()
        data = client.build_msg('raven.events.Exception', exc_info=data)
        exception.data = pickle.dumps(data)

        with transactional_session(Session) as session:
            session.add(exception)

    sys.excepthook = excepthook
