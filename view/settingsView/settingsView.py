import PySimpleGUI as sg
import createWindow as createWindow
import helpers.viewHelpers as view_helper
import app.services.settingsService.settingsService as service


class Settings:
    title = 'Settings'
    window_size = (1200, 500)
    t_b_color = '#2B2B28'

    file_location_layouts_define = []
    folder_location_layouts_define = ['recipes', 'library', 'mash compare export']
    view_layouts = view_helper.ViewHelper()
    browser_input_val = service.SettingsService().settings_list_to_object(service.SettingsService().get_settings())

    layout = [[
        view_layouts.generate_layout_for_path_browsers(
            folder_location_layouts_define,
            t_b_color,
            stored_input=browser_input_val),

        view_layouts.generate_layout_for_path_browsers(
            file_location_layouts_define, t_b_color,
            False,
            browser_input_val)
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

            if event == sg.WIN_CLOSED:
                self.window.close()
                break
            elif event == 'Cancel':
                self.view = 'main view'
                self.window.hide()
                self.window_hidden = True
                break
            elif event == '-Update-':
                service.SettingsService().update_settings_values(values)
                self.window['-Update-'].update(disabled=True)
            elif '_PATH-' in event:
                self.window['-Update-'].update(disabled=False)
