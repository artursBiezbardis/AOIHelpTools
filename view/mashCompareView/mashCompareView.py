import PySimpleGUI as sg
import createWindow as createWindow


class MashCompare:
    title = 'Select data and files to compare'
    mashCompareTable = []
    mashCompareTableHeadings = [
        'Name',
        'Part Number',
        'Description',
        'X-coord',
        'Y-coord',
        'Rotation',
        'Side',
        'Mount',
        'Type',
        'Remarks']

    layout = [
        [sg.Text('Check data needed to compare with check Buttons and browse mash files to compare')],
        [
            sg.CB('Name', default=True, disabled=True),
            sg.CB('Part Number', default=True),
            sg.CB('Description', default=True),
            sg.CB('X-cord', default=True),
            sg.CB('Y-cord', default=True),
            sg.CB('Rotation', default=True),
            sg.CB('Side', default=True)
        ],
        [
            [sg.Input(key='-FILE1-'), sg.FileBrowse(file_types=(("Excel Files", "*.xls"), ("Excel Files", "*.xlsx")))],
            [sg.Input(key='-FILE2-'), sg.FileBrowse(file_types=(("Excel Files", "*.xls"), ("Excel Files", "*.xlsx")))]
        ],
        [sg.B('Compare Mash Files', disabled=True), sg.Button('Cancel')],
        [sg.Table(mashCompareTable, headings=mashCompareTableHeadings, visible=False)]
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
            if event == sg.WIN_CLOSED:
                self.window.close()
                break
            elif event == 'Cancel':
                self.view = 'main view'
                self.window.hide()
                self.window_hidden = True
                break
