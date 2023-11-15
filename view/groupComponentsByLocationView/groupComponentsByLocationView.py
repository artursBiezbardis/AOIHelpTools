import PySimpleGUI as sg
import createWindow as createWindow
import helpers.helpers as helpers
import helpers.viewHelpers as view_helper
import app.services.groupComponentsByLocationService.goupComponentsByLocationService as group
import app.services.groupComponentsByLocationService.prepareRecipeToGroupComponentsService as prepareGroup


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
        sg.Text('STEP 1')
               ],
              [
        view_layouts.generate_layout_for_path_browsers(
            prepare_recipe_layout,
            t_b_color), sg.B('Recipe to prepare', key='-Prepare-', disabled=True, enable_events=True),
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
            sg.Text('STEP 2')
        ],
        [
            view_layouts.generate_layout_for_path_browsers(
                folder_location_layouts_define,
                t_b_color)
        ], [
            sg.Text('Suffix for part and package names', background_color=t_b_color, ),
            sg.Input(key='-SUFFIX-', size=20)
        ], [
            sg.Text('This setting is for adjusting area square border lines perpendicular position',
                    background_color=t_b_color, ),
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
                modified_recipe = group.GroupComponentsByLocation().main(input_data)
                sg.popup_get_text('recipe is created', title='Done', default_text=modified_recipe)
            elif event == '-RECIPE_TO_PREPARE_PATH-':
                self.window['-Prepare-'].update(disabled=False)
            elif event == '-Prepare-':
                recipe_paths = prepareGroup.PrepareRecipeToGroupComponentsService().main(
                    values['-RECIPE_TO_PREPARE_PATH-'])
                self.window[self.recipe_to_update].update(recipe_paths['group recipe'])
                self.window[self.read_locations].update(recipe_paths['locations recipe'])
                location_recipe = helpers.Helpers().get_filename_from_path(recipe_paths['locations recipe']).replace(
                    '.recipe', '')
                sg.popup_get_text(f'Steps to group components:\n'
                                  f'1.Open {location_recipe} recipe in cyberOptics software.\n'
                                  f'2.Open panel view and click on board tab.\n'
                                  f'3.Select first board in a boards list\n'
                                  f'4.Click Inspect Fids\n'
                                  f'5.Select Add -> Component\n'
                                  f'6.Draw around components you want to group\n'
                                  f'7.Save recipe and on save localize all parts and templates\n'
                                  f'8.Now you good to press OK , add suffix for components\n'
                                  f' and click on Create modified recipe button \n'
                                  , default_text=location_recipe)
                self.window['-Modify-'].update(disabled=False)
            if self.validate_input_prefix(
                    values[self.recipe_to_update],
                    'group'
            ) and self.validate_input_prefix(
                values[self.read_locations],
                'locations'
            ):
                self.window['-Modify-'].update(disabled=False)

    @staticmethod
    def validate_input_prefix(value: str, prefix: str) -> bool:
        helper = helpers.Helpers()
        file_name = helper.get_filename_from_path(value)
        prefix_from_file_name = (file_name.split('-'))[-1]
        result = True if prefix_from_file_name == prefix else False
        return result
