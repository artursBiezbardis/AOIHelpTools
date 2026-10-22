import PySimpleGUI as sg
import createWindow as createWindow
import app.services.settingsService.settingsService as settings
import app.services.compareRecipeMashServices.compareRecipeMashService as compareRecipeMash
import app.services.mashFileServices.exportMashToExcelService as exportExcel
import app.services.compareRecipeMashServices.updateRecipeComponentsFromMash as updateRecipe

class CompareRecipeMashView:
    get_settings = settings.SettingsService()
    title = 'Select mash and recipe to compare'
    window_size = (1200, 500)
    mash_compare_table = []
    table_headings = [
        'Component',
        'Recipe Part Name',
        'Mash Part Name',
        'Mash Mount',
        'Mash Type'
        ]

    layout = [
        [sg.Text('Check\'s if recipes component\'s parts name matches to recipe')],
        [
            [
                sg.Input(key='-FILE1-', enable_events=True),
                sg.FileBrowse(file_types=(("Recipes Files", "*.recipe"),),
                              initial_folder=get_settings.get_setting('-RECIPES_PATH-'))

            ],
            [
                sg.Input(key='-FILE2-', enable_events=True),
                sg.FileBrowse(file_types=(("Excel Files", "*.xls"), ("Excel Files", "*.xlsx")), initial_folder='Z:\cad')
            ]
        ],
        [
            sg.B('Compare Mash and Recipe', key='-COMPARE-', disabled=True, enable_events=True),
            sg.Button('Export to EXCEL', key='-EXCEL-', disabled=True, enable_events=True),
            sg.Button('Cancel')

        ],
        [sg.Table(
            mash_compare_table,
            key='-TABLE-',
            headings=table_headings,
            visible=False,
            col_widths=[24, 24, 8, 8, 8],
            expand_x=True,
            auto_size_columns=False,
            justification='center',
            vertical_scroll_only=False,
        )],
        [],
        [sg.Button('Update recipe diff', key='-UPDATE-', disabled=True, enable_events=True)],
        [sg.Checkbox('Remove components that are not in mash', key='-REMOVE_COMPONENTS-', enable_events=True),
         sg.Checkbox('Remove FOD\'S where components are removed', key='-REMOVE_FODS-', enable_events=True),
         sg.Checkbox('Add components that\'s are not in recipe', key='-ADD_COMPONENTS-', enable_events=True, disabled=True),
         ]


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

        compare = compareRecipeMash.CompareRecipeMashService()
        update_recipe = updateRecipe.UpdateRecipeComponentsFromMash()
        table = []
        actions = {}
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

            elif event == '-UPDATE-':
                actions['REMOVE_COMPONENTS'] = values['-REMOVE_COMPONENTS-']
                actions['REMOVE_FODS'] = values['-REMOVE_FODS-']
                actions['ADD_COMPONENTS'] = values['-ADD_COMPONENTS-']
                updateRecipe.UpdateRecipeComponentsFromMash().main(table, values['-FILE1-'], actions)
                #table = compare.main(values['-FILE1-'], values['-FILE2-'])
                #self.window['-TABLE-'].update(values=table, visible=True)
            elif event == '-EXCEL-':
                exportExcel.ExportToExcelService().create_excel(table[0], self.table_headings)
            elif event == '-COMPARE-':
                table = compare.main(values['-FILE1-'], values['-FILE2-'])
                self.window['-TABLE-'].update(values=table[0], visible=True)
                self.window['-EXCEL-'].update(disabled=False)
                if update_recipe.validate_table_for_update(table[0]):
                    self.window['-UPDATE-'].update(disabled=False)
            elif values['-FILE1-'] and values['-FILE2-']:
                self.window['-COMPARE-'].update(disabled=False)
            elif event == '-EXCEL-':
                exportExcel.ExportToExcelService().create_excel(table[0], self.table_headings)


