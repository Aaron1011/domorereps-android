from kivy.uix.widget import Widget
from kivy.clock import Clock
import math

class LongSliderEngine(Widget):

    def on_touch_down(self, x, timestamp):
        self.timer = None
        self.indices_per_pixel = 1.0 / self.cell_width
        self.min_middle_index = self.min_left_position * self.indices_per_pixel
        self.touch_began_position = x
        self.touch_began_middle_index = self.slider_inner.middle_index
        self.last_touch_velocity = 0.0
        self.last_touch_index = self.slider_inner.middle_index
        self.last_touch_timestamp = timestamp
        self.timer_callback = None

    def middle_index_for_x(self, x):
        possible_middle_index = self.touch_began_middle_index + (self.touch_began_position - x) * self.indices_per_pixel
        return max(self.min_middle_index, possible_middle_index)

    def reach_nearest(self, finish):
        velocity = 0.0
        if self.timer:
            self.timer = None
            if self.animation:
                velocity = self.animation.velocity

        animation = RubberBandAnimation()
        animation.end_index = max(0.0, math.floor(self.slider_inner.middle_index))
        animation.index = self.slider_inner.middle_index
        animation.velocity = velocity

        self.clock_callback = self.reach_nearest_timer_fires
        self.timer = Clock.schedule_interval(self.clock_callback,
                self.animation_period)
        self.animation = animation
        self.reach_nearest_finish_block = finish
        self.animation.start()

    def on_touch_move(self, x, timestamp):
        self.slider_inner.middle_index = self.middle_index_for_x(x)
        self.last_touch_velocity = (self.slider_inner.middle_index - self.last_touch_index) / (timestamp - self.last_touch_timestamp)
        self.last_touch_timestamp = timestamp

    def on_touch_up(self, x, timestamp):
        self.slider_inner.middle_index = self.middle_index_for_x(x)
        end_index = DecelerationAnimation(self.last_touch_index,
                self.last_touch_velocity)

        if round(end_index) == round(self.slider_inner.middle_index) or (
                self.slider_inner.middle_index < 0.0 and self.last_touch_velocity > 0.0
                and end_index <= 0.0):

            animation = RubberBandAnimation()
            animation.end_index = max(0.0. round(end_index))
        else:
            animation = DecelerationAnimation()
            animation.end_index = end_index
        animation.index = self.slider_inner.middle_index
        animation.velocity = self.last_touch_velocity
        self.last_touch_velocity = 0.0

        self.clock_callback = self.timer_fires
        self.timer = Clock.schedule_interval(self.clock_callback,
                self.animation_period)
        self.animation = animation
        self.animation.start()


    def reach_nearest_timer_fires(self):
        self.animation.advance()
        self.slider_inner.middle_index = self.animation.index
        if self.slider_inner.middle_index == self.animation.end_index:
            Clock.unschedule(self.clock_callback)
            self.timer = None
            self.reach_nearest_finish_block()


    def timer_fires(self):
        self.animation.advance()
        self.slider_inner.middle_index = self.animation.index
        if isinstance(self.animation, DecelerationAnimation):
            animation = None
            if round(self.slider_inner.middle_index) == round(self.animation.end_index):
                animation = RubberBandAnimation()
            elif self.slider_inner.middle_index < 0.0 and self.animation.velocity < 0.0:
                bounce_back_animation = BounceBackAnimation()
                bounce_back_animation.min_middle_index = self.min_middle_index
                animation = bounce_back_animation
            if animation != None:
                animation.end_index = max(0.0, round(self.animation.end_index))
                animation.index = self.slider_inner.middle_index
                animatiom.velocity = self.animation.velocity
                self.animation = animation
                self.animation.start()
        elif self.slider_inner.middle_index == self.animation.end_index:
            Clock.unschedule(self.clock_callback)
            self.timer = None
            self.animation = None

