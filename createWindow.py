import PySimpleGUI as simpleGui


class CreateWindow:
    resizable = True
    element_justification = 'center'

    def create(self, title: str, layout: list, size: tuple) -> object:
        simpleGui.theme('DarkGray2')

        return simpleGui.Window(
            title=title,
            layout=layout,
            size=size,
            resizable=self.resizable,
            element_justification=self.element_justification
        )
