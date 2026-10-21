class MashComponentModel:

    def __init__(self, mash_component_data):

        self.component = mash_component_data
        self.get_name()
        self.get_part_name()
        self.get_x_coordinate()
        self.get_y_coordinate()
        self.get_component_angle()
        self.get_side()
        self.get_mount()
        self.get_mount_type()
        self.get_description()
        self.get_comment()

    def get_name(self):
        return self.component[0]

    def get_part_name(self):
        return self.component[1]

    def get_x_coordinate(self):
        return self.component[3]

    def get_y_coordinate(self):
        return self.component[4]

    def get_component_angle(self):
        return self.component[5]

    def get_side(self):
        return self.component[6]

    def get_mount(self):
        return self.component[7]

    def get_mount_type(self):
        return self.component[8]

    def get_description(self):
        return self.component[2]

    def get_comment(self):
        return self.component[9]

    def get_list(self):
        return self.component





    
