import PySimpleGUI as sg
import createWindow as createWindow
import helpers.helpers
import helpers.viewHelpers as view_helper
import app.services.groupComponentsByLocationService.goupComponentsByLocationService as group
import  app.services.groupComponentsByLocationService.prepareRecipeToGroupComponentsService as prepareGroup

class GroupComponents:
    title = 'Grouping recipe components by location'
    window_size = (1200, 500)
    t_b_color = '#2B2B28'

    file_location_layouts_define = []
    folder_location_layouts_define = ['recipe folder to update', 'recipe folder for locations']
    prepare_recipe_layout = ['recipe to prepare']
    view_layouts = view_helper.ViewHelper()
    recipe_to_update = '-RECIPE_FOLDER_TO_UPDATE_PATH-'
    read_locations = '-RECIPE_FOLDER_FOR_LOCATIONS_PATH-'


    layout = [[
        view_layouts.generate_layout_for_path_browsers(
            folder_location_layouts_define,
            t_b_color)
    ], [
        sg.Text('Suffix for part and package names', background_color=t_b_color, ),
        sg.Input(key='-SUFFIX-', size=20)
    ], [
        sg.Text('This setting is for adjusting area square border lines perpendicular position', background_color=t_b_color, ),
    ], [
        sg.Text('Adjust offset on X coordinates outer vertical lines (mm)', background_color=t_b_color, ),
        sg.Input(0, key='-LEFT_OFFSET-', size=10),
        sg.Input(0, key='-RIGHT_OFFSET-', size=10),

    ], [
        sg.Text('Area Y offset outer horizontal lines (mm)', background_color=t_b_color, ),
        sg.Input(0, key='-UP_OFFSET-', size=10),
        sg.Input(0, key='-DOWN_OFFSET-', size=10),

    ], [
        sg.Text('Square offset (mm)', background_color=t_b_color, ),
        sg.Input(0, key='-X_OFFSET-', size=10),
        sg.Input(0, key='-Y_OFFSET-', size=10),

    ], [
            sg.B('Create modified recipe', key='-Modify-', disabled=True, enable_events=True),
            sg.Button('Cancel')

        ],
        [
            sg.Stretch(t_b_color)
        ],
        [
            sg.Stretch(t_b_color)
        ],
        [
            sg.Stretch()
        ],
        [
            sg.Stretch(t_b_color)
        ],
        [
            sg.Stretch(t_b_color)
        ],

        [
            view_layouts.generate_layout_for_path_browsers(
                prepare_recipe_layout,
                t_b_color), sg.B('Recipe to prepare', key='-Prepare-', disabled=True, enable_events=True),
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
                input_data = values
                group.GroupComponentsByLocation().main(input_data)

            elif self.validate_input_prefix(
                    values[self.recipe_to_update],
                    'group'
            ) and self.validate_input_prefix(
                values[self.read_locations],
                'locations'
            ):
                self.window['-Modify-'].update(disabled=False)
            elif event == '-RECIPE_TO_PREPARE_PATH-':
                self.window['-Prepare-'].update(disabled=False)
            elif event == '-Prepare-':
                prepareGroup.PrepareRecipeToGroupComponentsService().main(values['-RECIPE_TO_PREPARE_PATH-'])

    @staticmethod
    def validate_input_prefix(value: str, prefix: str) -> bool:
        helper = helpers.helpers.Helpers()
        file_name = helper.get_filename_from_path(value)
        prefix_from_file_name = (file_name.split('-'))[-1]
        result = True if prefix_from_file_name == prefix else False
        return result
