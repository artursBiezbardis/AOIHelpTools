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

    def contains_point(self, component_x: float, component_y: float) -> bool:
        return \
            (self.x - self.width/2) + self.left_line_offset <= component_x <=\
            (self.x + self.width/2) + self.right_line_offset and \
            (self.y-self.height/2) + self.down_line_offset <= component_y <= \
            self.y + self.height/2 + self.up_line_offset
