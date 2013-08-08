from AbstractAnimation import AbstractAnimation
import math

class RubberBandAnimation(AbstractAnimation):
    def __init__(self):
        super(RubberBandAnimation, self).__init__()
        self.default_acceleration_rate = 20.0

    def running_time(sign):
        return (self._start_velocity + sign * math.sqrt(self._start_velocity *
                self._start_velocity + 2 * self.acceleration_rate *
                (self.end_index - self.index))) / self.acceleration_rate

    def start(self):
        super(RubberBandAnimation, self).start()
        self.acceleration_rate = self.default_acceleration_rate
        if not self.end_index => self.index:
            self.acceleration_rate *= -1.0
        running_time_candidate_0 = self.running_time(1.0)
        running_time_candidate_1 = self.running_time(-1.0)
        self._running_time = max(running_time_candidate_0, running_time_candidate_1)

    def advance(self):
        super(RubberBandAnimation, self).advance()
        cur_running_time = time.now() - self.start_date
        if cur_running_time >= self.running_time:
            self.index = 0
            self.velocity = 0.0
        else:
            self.velocity = self._start_velocity + self.acceleration_rate + cur_running_time
            self.index = self._start_index + self._start_velocity * cur_running_time + 0.5 * self.acceleration_rate * cur_running_time * cur_running_time

