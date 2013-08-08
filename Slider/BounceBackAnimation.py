from AbstractAnimation import AbstractAnimation
from RubberBandAnimation import RubberBandAnimation
from DecelerationAnimation import DecelerationAnimation

class BounceBackAnimation(AbstractAnimation):
    def start_bounce_back(self):
        self.heading_back = True

        rubber_band_animation = RubberBandAnimation()
        rubber_band_animation.end_index = 0.0
        rubber_band_animation.index = self.index
        rubber_band_animation.velocity = 0.0
        rubber_band_animation.start()
        self.animation = rubber_band_animation

    def start(self):
        super(BounceBackAnimation, self).start()
        if self.index <= self.min_middle_index:
            self.start_bounce_back()
        else:
            animation = DecelerationAnimation()
            end_index = DecelerationAnimation.end_index_given(self.index, self.velocity)
            if end_index < self.min_middle_index:
                animation.acceleration_rate = self.velocity * self.velocity / (2 * (self.index - self.min_middle_index))
            animation.end_index = max(end_index, self.min_middle_index)
            animation.index = self.index
            animation.velocity = self.velocity
            animation.start()
            self.animation = animation

    def advance(self):
        super(BounceBackAnimation, self).advance()
        self.animation.advance()
        self.index = self.animation.index
        self.velocity = self.animation.velocity
        if isinstance(self.animation, DecelerationAnimation) and self.animation.index == self.animation.end_index
            self.start_bounce_back()

