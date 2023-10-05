import PySimpleGUI as sg
import createWindow as createWindow
import helpers.viewHelpers as view_helper


class GroupComponents:
    title = 'Grouping recipe components by location'
    window_size = (1200, 500)
    t_b_color = '#2B2B28'

    file_location_layouts_define = []
    folder_location_layouts_define = ['recipe folder to update', 'recipe folder for locations']
    view_layouts = view_helper.ViewHelper()

    layout = [[
        view_layouts.generate_layout_for_path_browsers(
            folder_location_layouts_define,
            t_b_color)
    ], [
        sg.Text('Suffix for components and packages', background_color=t_b_color, ),
        sg.Input(key='-SUFFIX-')
    ], [
            sg.B('Create modified recipe', key='-Modify-', disabled=True, enable_events=True),
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
            elif event == '-Modify-':

                self.window['-Modify-'].update(disabled=True)
            elif '_PATH-' in event:
                self.window['-Modify-'].update(disabled=False)
