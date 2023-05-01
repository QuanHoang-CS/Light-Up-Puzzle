from CellState import *


class Cell:
    def __init__(self, x_coord, y_coord, value):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.value = value

        if self.value.isdigit():
            self.domain = [CellState.WALL]
        elif self.value == '_':
            self.domain = [CellState.BULB, CellState.EMPTY]

    def get_cell_position(self):
        return [self.x_coord, self.y_coord]

    def get_cell_value(self):
        return self.value

    def is_wall(self):
        return self.state.isdigit()

    def is_bulb(self):
        return self.value == CellState.BULB

    def is_empty(self):
        return self.value == CellState.EMPTY

    def is_light(self):
        return self.value == CellState.LIGHT

    def has_domain_of_size_zero(self):
        return len(self.domain) == 0

    def get_cell_domain(self):
        return self.domain

    def get_domain_size(self):
        return len(self.domain)

    def domain_contain(self, value):
        return value in (self.domain)

    def remove_bulb_from_domain(self):
        if CellState.BULB in self.domain:
            self.domain.remove(CellState.BULB)

    def set_cell_value(self, new_value):
        self.value = new_value