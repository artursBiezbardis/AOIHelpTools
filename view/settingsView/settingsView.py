import PySimpleGUI as sg
import createWindow as createWindow
import app.repositories.sqlLiteRepository.sqlLiteRepository as sqlLite


class Settings:
    data_base = 'C:\\Users\\arturs.biezbardis\\PycharmProjects\\AOIHelpTools\\settings.db'
    title = 'Settings'
    window_size = (1200, 500)
    recipes_folder = sqlLite.SQLiteRepository().read_value_by_name('setup', 'recipes_folder', data_base)
    mash_compare_excel_export_folder = 'xxxx'

    layout = [
        [
            [
                sg.Input(recipes_folder, key='-Recipes-', enable_events=True),
                sg.FolderBrowse()
            ],
            [
                sg.Input(mash_compare_excel_export_folder, key='-FILE2-', enable_events=True),
                sg.FolderBrowse()
            ]
        ],
        [
            sg.B('Update settings', key='-Update-', disabled=True, enable_events=True),
            sg.Button('Cancel')

        ],

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

            settings_collection = []

            if event == sg.WIN_CLOSED:
                self.window.close()
                break
            elif event == 'Cancel':
                self.view = 'Settings'
                self.window.hide()
                self.window_hidden = True
                break
            elif event == '-Update-':
                sqlLite.SQLiteRepository().set_value_by_name(
                    'setup',
                    'recipes_folder',
                     self.data_base,
                     values['-Recipes-']
                )
                input_value = sqlLite.SQLiteRepository().read_value_by_name(
                    'setup',
                    'recipes_folder',
                    self.data_base
                )
                self.window['-Recipes-'].update(input_value)
            elif values['-Recipes-'] is not self.recipes_folder :
                self.window['-Update-'].update(disabled=False)



    def collect_all_settings (self, values):

        return

