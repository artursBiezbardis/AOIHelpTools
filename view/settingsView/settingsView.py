import PySimpleGUI as sg
import createWindow as createWindow
import app.repositories.sqlLiteRepository.sqlLiteRepository as sqlLite
import helpers.viewHelpers as view_helper
import app.services.settingsService.settingsService as service


class Settings:
    title = 'Settings'
    window_size = (1200, 500)
    t_b_color = '#2B2B28'

    data_base = 'C:\\Users\\arturs.biezbardis\\PycharmProjects\\AOIHelpTools\\settings.db'
    settings_table = 'setup'
    all_settings = service.SettingsService().settings_list_to_object(
        sqlLite.SQLiteRepository().get_all_settings(settings_table, data_base))
    recipes_folder = sqlLite.SQLiteRepository().read_value_by_name(settings_table, '-RECIPES_PATH-', data_base)
    file_location_layouts_define = ['database']
    folder_location_layouts_define = ['recipes', 'library', 'mash compare export']
    view_layouts = view_helper.ViewHelper()

    layout = [[
        view_layouts.generate_layout_for_path_browsers(folder_location_layouts_define, t_b_color, all_settings),
        view_layouts.generate_layout_for_path_browsers(file_location_layouts_define, t_b_color, all_settings, False)
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
            settings_list = sqlLite.SQLiteRepository().get_all_settings(self.settings_table, self.data_base)

            if event == sg.WIN_CLOSED:
                self.window.close()
                break
            elif event == 'Cancel':
                self.view = 'main view'
                self.window.hide()
                self.window_hidden = True
                break
            elif event == '-Update-':
                for name, val in settings_list:
                    if val is not values[name]:
                        sqlLite.SQLiteRepository().set_value_by_name(
                            self.settings_table,
                            name,
                            self.data_base,
                            values[name]
                        )
                        input_value = sqlLite.SQLiteRepository().read_value_by_name(
                            self.settings_table,
                            name,
                            self.data_base
                        )
                        self.window[name].update(input_value)
            elif values['-RECIPES_PATH-'] is not self.recipes_folder:
                self.window['-Update-'].update(disabled=False)

    def settings_list_to_object(self, all_settings):
        all_settings_obj = {}
        for name, val in all_settings:
            all_settings_obj[name] = val

        return all_settings_obj
