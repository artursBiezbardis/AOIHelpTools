import PySimpleGUI as sg


class CreateWindow:
    resizable = True
    element_justification = 'center'

    def create(self, title: str, layout: list, size: tuple) -> object:
        sg.theme('DarkGray2')

        return sg.Window(
            title=title,
            layout=layout,
            size=size,
            resizable=self.resizable,
            element_justification=self.element_justification
        )
