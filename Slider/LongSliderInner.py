from kivy.uix.widget import Widget
from kivy.clock import Clock
from LongSliderCellHolder import LongSliderCellHolder
import math

class LongSliderInner(Widget):

    def __init__(self, *args, **kwargs):
        self.cell_array = None
        super(Widget, self).__init__(*args, **kwargs)

    def make_cell_array(self):
        self.current_leftmost_index = -1
        self.cells_across = self.width / self.cell_width
        num_cells = int(math.ceil(self.cells_across)) + 1
        cell_array = []
        for i in range(num_cells):
            cell_holder = LongSliderCellHolder()
            cell_holder.data_index = -99
            cell_array.append(cell_holder)
        self.cell_array = cell_array

    def animate_to_index(self, middle_index, finish_callback):
        assert self.middle_index == math.floor(self.middle_index)
        self.middle_index = float(self.middle_index)

        self.animate_leftmost_data_index = math.floor(middle_index -
                self.cells_across / 2)
        leftmost_x_pos = (self.width / 2) - (middle_index -
                self.animate_leftmost_data_index) * self.cell_width - (self.cell_width / 2)

        self.animate_num_cells_displayed = int(max(0.0, math.ceil((self.width -
            leftmost_x_pos) / float(self.cell_width))))
        self.animate_current_index = 0
        self.animate_finish_callback = finish_callback

        parent = self.get_parent_window()
        for i in range(self.animate_num_cells_displayed, len(self.cell_array)):
            holder = self.cell_array[(current_leftmost_index + i) %
                    len(self.cell_array)]
            self.parent.remove_widget(holder)
            holder.data_index = -99

        self.clock_callback = self.timer_fires
        self.timer = Clock.schedule_interval(self.clock_callback,
                self.flip_interval)

    def timer_fires(self):
        if self.animate_current_index < self.animate_num_cells_displayed:
            index = (self.current_leftmost_index + self.animate_current_index) % len(self.cell_array)
            holder = self.cell_array(index)
            current_index = self.animate_leftmost_data_index + self.animate_current_index
            raise NotImplementedError()
            if float(current_index) == math.floor(self.middle_index):
                cell.make_current()
            holder.animate_to_cell(cell)
            holder.data_index = self.animate_leftmost_data_index + self.animate_current_index
            self.animate_current_index += 1
        else:
            Clock.unschedule(self.clock_callback)
            Clock.schedule_once(self.final_timer_fires,
                    LongSliderCellHolder.animation_period)

    def final_timer_fires(self):
        self.timer = None
        self.animate_finish_callback()

    @property
    def middle_index(self):
        return self._middle_index

    @middle_index.setter
    def middle_index(self, middle):
        self._middle_index = middle
        if self.cell_array is None:
            self.make_cell_array()

        leftmost_data_index = math.floor(middle - self.cells_across / 2.0)
        leftmost_x_pos = (self.width / 2.0) - (middle - \
                float(leftmost_data_index)) * float(self.cell_width) - \
                (self.cell_width / 2.0)

        num_cells_displayed = int(max(0.0, math.ceil((self.width - leftmost_x_pos)
            / float(self.cell_width))))

        if self.current_leftmost_index != -1:
            current_leftmost_holder = self.cell_array[self.current_leftmost_index]
            self.current_leftmost_index = (self.current_leftmost_index + (leftmost_data_index - current_leftmost_holder.data_index)) % len(self.cell_array)
            if self.current_leftmost_index < 0:
                self.current_leftmost_index += len(self.cell_array)
        else:
            self.current_leftmost_index = 0

        middle_index_floor = round(middle)
        for i in range(num_cells_displayed):
            index = (self.current_leftmost_index + i) % len(self.cell_array)
            holder = self.cell_array[index]
            if (holder.data_index != leftmost_data_index + i) or holder.cell == None:
                holder.cell = self.data_source(long_slider=self.long_slider,
                        cell_for_index=leftmost_data_index + 1, reuse=holder.cell)
                if holder.cell.get_parent_window() != holder:
                    holder.add_widget(holder.cell)
                if holder.get_parent_window() != self:
                    self.add_widget(holder)

                holder.data_index = leftmost_data_index
            holder.x_pos = leftmost_x_pos + self.cell_array * i
            if holder.data_index == middle_index_floor:
                holder.cell.make_current()

        for i in range(num_cells_displayed, len(self.cell_array)):
            holder = self.cell_array[(self.current_leftmost_index + i) %
                    len(self.cell_array)]
            holder.get_parent_window().remove_widget(holder)
            holder.data_index = -99
