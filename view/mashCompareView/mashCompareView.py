import PySimpleGUI as sg
import createWindow as createWindow
import app.services.mashFileServices.mashFileService as mashService
import app.services.mashFileServices.exportMashToExcelService as exportExcel


class MashCompare:
    title = 'Select data and files to compare'
    window_size = (1200, 500)
    mashCompareTable = []
    mashCompareTableHeadings = [
        'Mash',
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
            sg.CB('Part Number', default=True, enable_events=True, key="-PART_NUMBER-", ),
            sg.CB('Description', default=True, enable_events=True, key="-DESCRIPTION-"),
            sg.CB('X-cord', default=True, enable_events=True, key="-X_CORD-"),
            sg.CB('Y-cord', default=True, enable_events=True, key="-Y_CORD-"),
            sg.CB('Rotation', default=True, enable_events=True, key="-ROTATION-"),
            sg.CB('Side', default=True, enable_events=True, key="-SIDE-")
        ],
        [
            [
                sg.Input(key='-FILE1-', enable_events=True),
                sg.FileBrowse(file_types=(("Excel Files", "*.xls"), ("Excel Files", "*.xlsx")))
            ],
            [
                sg.Input(key='-FILE2-', enable_events=True),
                sg.FileBrowse(file_types=(("Excel Files", "*.xls"), ("Excel Files", "*.xlsx")))
            ]
        ],
        [
            sg.B('Compare Mash Files', key='-COMPARE-', disabled=True, enable_events=True),
            sg.Button('Export to EXCEL', key='-EXCEL-', disabled=True, enable_events=True),
            sg.Button('Cancel')

        ],
        [sg.Table(
            mashCompareTable,
            key='-TABLE-',
            headings=mashCompareTableHeadings,
            visible=False,
            col_widths=[24, 5, 8, 30, 6, 6, 5, 10, 10, 15],
            expand_x=True,
            auto_size_columns=False,
            justification='center',
            vertical_scroll_only=False,
        )],
        []

    ]

    def __init__(self):
        self.view = ''
        self.window = createWindow.CreateWindow.create(
            createWindow.CreateWindow(),
            self.title,
            self.layout,
            self.window_size)
        self.window_hidden = False

    def run_window(self):

        if self.window_hidden:
            self.window.un_hide()
        while True:
            event, values = self.window.read()
            setEmptyCellsToMashFiles = {
                '-PART_NUMBER-': values['-PART_NUMBER-'],
                '-DESCRIPTION-': values['-DESCRIPTION-'],
                '-X_CORD-': values['-X_CORD-'],
                '-Y_CORD-': values['-Y_CORD-'],
                '-ROTATION-': values['-ROTATION-'],
                '-SIDE-': values['-SIDE-']
            }

            if event == sg.WIN_CLOSED:
                self.window.close()
                break
            elif event == 'Cancel':
                self.view = 'main view'
                self.window.hide()
                self.window_hidden = True
                break
            elif event == '-EXCEL-':
                exportExcel.ExportToExcelService().create_excel(table, self.mashCompareTableHeadings,)
            elif event == '-COMPARE-':
                table = (mashService.MashFileService().compare_two_mashes(values['-FILE1-'], values['-FILE2-'], setEmptyCellsToMashFiles))[0]
                self.window['-TABLE-'].update(values=table, visible=True)
                self.window['-EXCEL-'].update(disabled=False)
            elif values['-FILE1-'] and values['-FILE2-']:
                self.window['-COMPARE-'].update(disabled=False)
            elif event == '-EXCEL-':
                exportExcel.ExportToExcelService().create_excel(table, self.mashCompareTableHeadings)
