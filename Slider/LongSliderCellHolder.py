from kivy.uix.widget import Widget

class LongSliderCellHolder(Widget):

    def __init__(self, *args, **kwargs):
        self.cell = None
        super(LongSliderCellHolder, self).__init__()

    def animate_to_cell(self, cell):
        pass
