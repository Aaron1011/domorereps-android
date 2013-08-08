from kivy.uix.widget import Widget
from LongSliderInner import LongSliderInner
from LongSliderEngine import LongSliderEngine

class LongSlider(Widget):
    def __init__(self):
        super(LongSlider, self).__init__()
        self.data_source = None
        self.delegate = None
        self.default_index = 0
        self.default_cell_width = 50
        self.cell_width = 50
        self.long_slider_engine = None
        self.slider_inner = None
        self.animating = False

        self.setup_slider()

    def on_touch_down(self, touch):
        if self.animating:
            return
        self.long_slider_engine.on_touch_down(touch.x, touch.time_start)

    def on_touch_move(self, touch):
        if self.animating:
            return
        self.long_slider_engine.on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.animating:
            return
        self.long_slider_engine.on_touch_up(touch)

    def animate_to_index(self, middle_index, data_source):
        self.animating = True
        def finish_block():
            self.slider_inner.data_source = self.data_source
            self.slider_inner.animate_to_index(middle_index,
                    finish_callback=animation_finished)

        self.long_slider_engine.reach_nearest(finish_block)


    def animation_finished(self):
        self.animating = False



    def setup_slider(self):
        if not self.long_slider_engine:
            self.long_slider_engine = LongSliderEngine()
            self.long_slider_engine.default_index = self.default_index
            self.long_slider_engine.cell_width = self.cell_width

            slider_inner = LongSliderInner()
            self.long_slider_engine.slider_inner = slider_inner
            slider_inner.long_slider = self
            slider_inner.cell_width = self.cell_width
            slider_inner.data_source = self.data_source
            slider_inner.middle_index = self.default_index

