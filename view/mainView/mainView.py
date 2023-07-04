import createWindow as createWindow
import PySimpleGUI as sg


class MainView:
    title: str = 'main view'
    button1Title: str = 'Compare Mash'
    buttonCancelTitle: str = 'Cancel'
    layout: [[sg.Button]] = [[sg.Button(button1Title), sg.Button(buttonCancelTitle)]]

    def __init__(self):
        self.view = ''
        self.window = createWindow.CreateWindow.create(self.title, self.layout)
    def run_window(self):

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                self.window.close()
                break

            elif event == 'Compare Mash':

                self.view = event
                self.window.close()
                break

            print('You entered ', values[0])
            self.window.close()



    def get_event(self):
        test = self.view

        return test
