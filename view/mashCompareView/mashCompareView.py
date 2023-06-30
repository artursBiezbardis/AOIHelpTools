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
        [sg.B('Compare Mash Files'), sg.Button('Cancel')]
    ]

    def run_window(self):
        window = createWindow.CreateWindow.create(self.title, self.layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Compare Mash':  # if user closes window or clicks cancel
                break

            print('You entered ', values[0])
        window.close()
