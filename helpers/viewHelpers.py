import PySimpleGUI as sg


class ViewHelper:

    def generate_layout_for_path_browsers(
            self,
            input_layouts,
            text_background_color=None,
            folder_browser=True,
            stored_input=[]
    ):

        layouts = []

        for val in input_layouts:
            val_to_upper_case = val.upper().replace(' ', '_')
            val_first_upper_case = val.capitalize()
            name = '-' + val_to_upper_case + '_PATH-'

            layouts.append(
                [sg.Text(
                    self.string_length_adjustment_with_white_space(val_first_upper_case, 50, ' path'),
                    background_color=text_background_color
                ),
                 sg.Input(
                     default_text=('' if stored_input == [] else stored_input[name]),
                     key=name,
                     enable_events=True
                 ),
                 sg.FolderBrowse() if folder_browser else sg.FileBrowse()
                 ]
            )
        return layouts

    def string_length_adjustment_with_white_space(self, string:str, length:int, additional_string='') -> str:
        string = string+additional_string
        string_length =len(string)
        for i in range(length):
            if i >= string_length:
                string += ' '

        return string
