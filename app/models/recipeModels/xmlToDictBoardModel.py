class XmlToDictBoardModel:

    def __init__(self, board_data):
        self.data = board_data
        self.get_board_data()
        self.get_board_components()
        self.get_board_nr()
        self.get_board_angle()
        self.get_board_position_x()
        self.get_board_position_y()
        self.get_board_height()
        self.get_board_width()

    def get_all_board_data(self):

        return self.data

    def get_board_data(self):

        return self.get_all_board_data()['Board']

    def get_board_components(self):

        return self.get_board_data()['Children']['a:Element']

    def get_board_nr(self):

        return self.get_board_data()['Name']['#text']

    def get_board_angle(self):

        return int(self.get_board_data()['RotationZ']['#text']) if 'RotationZ' in self.get_board_data() else 0

    def get_board_position_x(self):

        return float(self.get_board_data()['Position']['X'])

    def get_board_position_y(self):

        return float(self.get_board_data()['Position']['Y'])

    def get_board_height(self):

        return float(self.get_board_data()['BoardHeight'])

    def get_board_width(self):

        return float(self.get_board_data()['BoardWidth'])

    def _set_board_data(self, board_data):
        self.data['Board'] = board_data

    def set_board_components(self, components):
        board_data = self.get_board_data()
        board_data['Children']['a:Element'] = components
        self._set_board_data(board_data)
