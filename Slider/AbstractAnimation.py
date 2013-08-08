from datetime import datetime

class AbstractAnimation(object):
    def __init__(self):
        self.index = None
        self.end_index = None
        self.velocity = None
        self.animation_period = 0.02

    def start(self):
        self.start_date = datetime.now()
        self._start_index = self.index
        self._start_velocity = self.velocity

    def advance(self):
        raise NotImplementedError()
