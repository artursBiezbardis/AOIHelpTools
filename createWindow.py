import PySimpleGUI as sg


class CreateWindow:

    @staticmethod
    def create(title: str, layout: list) -> object:
        sg.theme('DarkGray2')

        return sg.Window(title=title, layout=layout)
