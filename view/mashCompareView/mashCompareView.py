import createWindow as ui
import app.services.mashFileServices.mashFileService as mashService
import app.services.mashFileServices.exportMashToExcelService as exportExcel


class MashCompare:
    title = 'Select data and files to compare'
    window_size = (1200, 560)
    mash_compare_table_headings = [
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
        'Remarks'
    ]

    layout = [
        [ui.text('Check the values to compare, then choose two mash files')],
        [
            ui.checkbox('Name', key='-NAME-', default=True, disabled=True),
            ui.checkbox('Part Number', key='-PART_NUMBER-', default=True, enable_events=True),
            ui.checkbox('Description', key='-DESCRIPTION-', default=True, enable_events=True),
            ui.checkbox('X-cord', key='-X_CORD-', default=True, enable_events=True),
            ui.checkbox('Y-cord', key='-Y_CORD-', default=True, enable_events=True),
            ui.checkbox('Rotation', key='-ROTATION-', default=True, enable_events=True),
            ui.checkbox('Side', key='-SIDE-', default=True, enable_events=True),
        ],
        [
            ui.input_box('-FILE1-', enable_events=True, expand=True),
            ui.file_browse((("Excel files", "*.xls"), ("Excel files", "*.xlsx"))),
        ],
        [
            ui.input_box('-FILE2-', enable_events=True, expand=True),
            ui.file_browse((("Excel files", "*.xls"), ("Excel files", "*.xlsx"))),
        ],
        [
            ui.button('Compare Mash Files', key='-COMPARE-', disabled=True),
            ui.button('Export to EXCEL', key='-EXCEL-', disabled=True),
            ui.button('Cancel'),
        ],
        [ui.table('-TABLE-', mash_compare_table_headings, visible=False)],
    ]

    def __init__(self):
        self.view = ''
        self.window = ui.CreateWindow().create(self.title, self.layout, self.window_size)
        self.window_hidden = True

    def run_window(self):
        table = []
        cells_with_differences = []
        if self.window_hidden:
            self.window.un_hide()
            self.window_hidden = False
        while True:
            event, values = self.window.read()
            if event is None:
                self.window.close()
                break
            if event == 'Cancel':
                self.view = 'main view'
                self.window.hide()
                self.window_hidden = True
                break

            compared_columns = {
                '-PART_NUMBER-': values['-PART_NUMBER-'],
                '-DESCRIPTION-': values['-DESCRIPTION-'],
                '-X_CORD-': values['-X_CORD-'],
                '-Y_CORD-': values['-Y_CORD-'],
                '-ROTATION-': values['-ROTATION-'],
                '-SIDE-': values['-SIDE-'],
            }
            if event == '-EXCEL-' and table:
                exportExcel.ExportToExcelService().create_excel(
                    table,
                    self.mash_compare_table_headings,
                    cells_with_differences,
                )
            elif event == '-COMPARE-':
                table, cells_with_differences = mashService.MashFileService().compare_two_mashes(
                    values['-FILE1-'], values['-FILE2-'], compared_columns
                )
                self.window['-TABLE-'].update(values=table, visible=True)
                self.window['-EXCEL-'].update(disabled=False)
            elif values['-FILE1-'] and values['-FILE2-']:
                self.window['-COMPARE-'].update(disabled=False)
