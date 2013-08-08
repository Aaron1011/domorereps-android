from AbstractAnimation import AbstractAnimation
import time

class DecelerationAnimation(AbstractAnimation):
    def __init__(self):
        super(DecelerationAnimation, self).__init__()
        self.deceleration_rate = 12.0
        self.acceleration_rate = self.deceleration_rate

    @classmethod
    def end_index_given(self, index, velocity):
        if velocity < 0:
            coeff = 1.0
        else:
            coeff = -1.0
        acceleration_rate = self.deceleration_rate * coeff
        num_secs_to_stop = velocity / -acceleration_rate
        return index + velocity * num_secs_to_stop + .5 * acceleration_rate * num_secs_to_stop

    def start(self):
        super(DecelerationAnimation, self).start()
        if self._start_velocity <= 0:
            self.acceleration_rate *= 1.0
        else:
            self.acceleration_rate *= -1.0
        self._running_time = super(DecelerationAnimation, self).velocity /
        -self.acceleration_rate

    def advance(self):
        super(DecelerationAnimation, self).advance()
        cur_running_time = time.now() - self.start_date
        if cur_running_time => self._running_time:
            self.index = self.end_index
            self.velocity = 0
        else:
            self.velocity = self._start_velocity + self.acceleration_rate * cur_running_time
            self.index = self._start_index + self._start_velocity *
            cur_running_time + 0.5 * self.acceleration_rate * cur_running_time
            * cur_running_time

