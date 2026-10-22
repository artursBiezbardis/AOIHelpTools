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
        half_width = self.width / 2
        half_height = self.height / 2
        self.min_x = (self.x - half_width) + self.left_line_offset
        self.max_x = (self.x + half_width) + self.right_line_offset
        self.min_y = (self.y - half_height) + self.down_line_offset
        self.max_y = (self.y + half_height) + self.up_line_offset

    def check_contains_component(self, component_x: float, component_y: float) -> bool:
        return self.min_x <= component_x <= self.max_x and self.min_y <= component_y <= self.max_y
