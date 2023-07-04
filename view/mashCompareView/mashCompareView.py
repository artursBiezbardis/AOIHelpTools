import PySimpleGUI as sg
import createWindow as createWindow

class MashCompare:
    title = 'Select data and files to compare'
    layout = [
        [sg.Text('Check data needed to compare with check Buttons and browse mash files to compare')],
        [
            sg.CB('Name', default=True),
            sg.CB('Part Number', default=True),
            sg.CB('Description', default=True),
            sg.CB('X-cord', default=True),
            sg.CB('Y-cord', default=True),
            sg.CB('Rotation', default=True),
            sg.CB('Side', default=True)
        ],
        [
            [sg.Input(key='-FILE1-'), sg.FileBrowse()],
            [sg.Input(key='-FILE2-'), sg.FileBrowse()]
        ],
        [sg.B('Compare Mash Files'), sg.Button('Cancel')]
    ]

    def __init__(self):
        self.view = ''
        self.window = createWindow.CreateWindow.create(self.title, self.layout)
        self.window_hidden = False
    def run_window(self):
        if self.window_hidden:

            self.window.un_hide()

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                self.window.close()
                break
            elif event == 'Cancel':
                self.view = 'main view'
                self.window.hide()
                self.window_hidden = True
                break

            print('You entered ', values[0])
