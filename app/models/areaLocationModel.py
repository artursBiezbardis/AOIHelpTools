from dataclasses import dataclass


@dataclass
class AreaLocation:
    location_name: str
    x: float
    y: float
    width: float
    height: float
    offset_x: float
    offset_y: float
    left_line_offset: float
    right_line_offset: float
    up_line_offset: float
    down_line_offset: float

    def __post_init__(self):
        self._min_x = (self.x - self.width / 2) + self.left_line_offset
        self._max_x = (self.x + self.width / 2) + self.right_line_offset
        self._min_y = (self.y - self.height / 2) + self.down_line_offset
        self._max_y = self.y + self.height / 2 + self.up_line_offset

    def check_contains_component(self, component_x: float, component_y: float) -> bool:
        return self._min_x <= component_x <= self._max_x and self._min_y <= component_y <= self._max_y
