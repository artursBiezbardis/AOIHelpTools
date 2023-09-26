import createWindow as createWindow
import PySimpleGUI as sg


class MainView:
    title: str = 'main view'
    button1Title: str = 'Compare Mash'
    buttonCancelTitle: str = 'Cancel'
    button2Title: str = 'Find Recipes by Part'
    buttonSettings:str = 'Settings'
    window_size = (500, 50)
    layout: [[sg.Button]] = [[
        sg.Button(button1Title),
        sg.Button(button2Title),
        sg.Button(buttonSettings),
        sg.Button(buttonCancelTitle)
    ]]

    def __init__(self):
        self.view = ''
        self.window = createWindow.CreateWindow.create(
            createWindow.CreateWindow(),
            self.title,
            self.layout,
            self.window_size
        )
        self.window_hidden = False

    def run_window(self):

        while True:

            if self.window_hidden:
                self.window.un_hide()
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.view = ''

                break

            elif event == 'Compare Mash':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break

            elif event == 'Find Recipes by Part':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break

            elif event == 'Settings':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break

            self.window.close()

    def get_event(self):
        test = self.view

        return test
