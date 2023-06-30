import createWindow as createWindow
import PySimpleGUI as sg


class MainView:
    title: str = 'main view'
    button1Title: str = 'Compare Mash'
    buttonCancelTitle: str = 'Cancel'
    layout: [[sg.Button]] = [[sg.Button(button1Title), sg.Button(buttonCancelTitle)]]

    def __init__(self):
        self.view = ''

    def run_window(self):
        test = sg.read_all_windows()

        window = createWindow.CreateWindow.create(self.title, self.layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel

                break

            elif event == 'Compare Mash':

                self.view = event

                break

            print('You entered ', values[0])
            window.close()



    def get_event(self):
        test = self.view

        return test
