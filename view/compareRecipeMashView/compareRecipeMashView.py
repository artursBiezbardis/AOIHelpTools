import os

import createWindow as ui
import app.services.settingsService.settingsService as settings
import app.services.compareRecipeMashServices.compareRecipeMashService as compareRecipeMash
import app.services.mashFileServices.exportMashToExcelService as exportExcel
import app.services.compareRecipeMashServices.updateRecipeComponentsFromMash as updateRecipe


def _existing_folder(path):
    if path and os.path.isdir(path):
        return path
    return None


class CompareRecipeMashView:
    get_settings = settings.SettingsService()
    title = 'Select mash and recipe to compare'
    window_size = (1100, 640)
    table_headings = [
        'Component',
        'Recipe Part Name',
        'Mash Part Name',
        'Mash Mount',
        'Mash Type',
    ]

    layout = [
        [ui.text("Checks if a recipe component's part name matches the mash")],
        [
            ui.input_box('-FILE1-', enable_events=True, expand=True),
            ui.file_browse(
                (("Recipe files", "*.recipe"),),
                initial_folder=_existing_folder(get_settings.get_setting('-RECIPES_PATH-')),
            ),
        ],
        [
            ui.input_box('-FILE2-', enable_events=True, expand=True),
            ui.file_browse(
                (("Excel files", "*.xls"), ("Excel files", "*.xlsx")),
                initial_folder=_existing_folder('Z:\\cad'),
            ),
        ],
        [
            ui.button('Compare Mash and Recipe', key='-COMPARE-', disabled=True),
            ui.button('Export to EXCEL', key='-EXCEL-', disabled=True),
            ui.button('Cancel'),
        ],
        [ui.table('-TABLE-', table_headings, visible=False, height=14)],
        [ui.button('Update recipe diff', key='-UPDATE-', disabled=True)],
        [
            ui.checkbox('Remove components that are not in mash', key='-REMOVE_COMPONENTS-', enable_events=True),
            ui.checkbox("Remove FOD's where components are removed", key='-REMOVE_FODS-', enable_events=True),
            ui.checkbox("Add components that are not in recipe", key='-ADD_COMPONENTS-', enable_events=True, disabled=True),
        ],
    ]

    def __init__(self):
        self.view = ''
        self.window = ui.CreateWindow().create(self.title, self.layout, self.window_size)
        self.window_hidden = True

    def run_window(self):
        compare = compareRecipeMash.CompareRecipeMashService()
        update_recipe = updateRecipe.UpdateRecipeComponentsFromMash()
        table = []
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
            if event == '-UPDATE-':
                actions = {
                    'REMOVE_COMPONENTS': values['-REMOVE_COMPONENTS-'],
                    'REMOVE_FODS': values['-REMOVE_FODS-'],
                    'ADD_COMPONENTS': values['-ADD_COMPONENTS-'],
                }
                updateRecipe.UpdateRecipeComponentsFromMash().main(table, values['-FILE1-'], actions)
            elif event == '-EXCEL-' and table:
                exportExcel.ExportToExcelService().create_excel(table[0], self.table_headings)
            elif event == '-COMPARE-':
                table = compare.main(values['-FILE1-'], values['-FILE2-'])
                self.window['-TABLE-'].update(values=table[0], visible=True)
                self.window['-EXCEL-'].update(disabled=False)
                if update_recipe.validate_table_for_update(table[0]):
                    self.window['-UPDATE-'].update(disabled=False)
            elif values['-FILE1-'] and values['-FILE2-']:
                self.window['-COMPARE-'].update(disabled=False)
