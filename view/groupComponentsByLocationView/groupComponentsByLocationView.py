import createWindow as ui
import helpers.helpers as helpers
import helpers.viewHelpers as view_helper
import app.services.groupComponentsByLocationService.goupComponentsByLocationService as group
import app.services.groupComponentsByLocationService.prepareRecipeToGroupComponentsService as prepareGroup


class GroupComponents:
    title = 'Grouping recipe components by location'
    window_size = (1100, 640)
    t_b_color = '#2B2B28'

    folder_location_layouts_define = ['recipe folder to update', 'recipe folder for locations']
    prepare_recipe_layout = ['recipe to prepare']
    view_layouts = view_helper.ViewHelper()
    recipe_to_update = '-RECIPE_FOLDER_TO_UPDATE_PATH-'
    read_locations = '-RECIPE_FOLDER_FOR_LOCATIONS_PATH-'

    layout = [
        [ui.text('STEP 1')],
        [
            view_layouts.generate_layout_for_path_browsers(prepare_recipe_layout, t_b_color),
            ui.button('Recipe to prepare', key='-Prepare-', disabled=True),
        ],
        [ui.text('STEP 2')],
        [view_layouts.generate_layout_for_path_browsers(folder_location_layouts_define, t_b_color)],
        [
            ui.text('Suffix for part and package names', t_b_color),
            ui.input_box('-SUFFIX-', width=20),
        ],
        [ui.text('This setting is for adjusting area square border lines perpendicular position', t_b_color)],
        [
            ui.text('Adjust offset on X coordinates outer vertical lines (mm)', t_b_color),
            ui.input_box('-LEFT_OFFSET-', default='0', width=10),
            ui.input_box('-RIGHT_OFFSET-', default='0', width=10),
        ],
        [
            ui.text('Area Y offset outer horizontal lines (mm)', t_b_color),
            ui.input_box('-UP_OFFSET-', default='0', width=10),
            ui.input_box('-DOWN_OFFSET-', default='0', width=10),
        ],
        [
            ui.text('Square offset (mm)', t_b_color),
            ui.input_box('-X_OFFSET-', default='0', width=10),
            ui.input_box('-Y_OFFSET-', default='0', width=10),
        ],
        [
            ui.button('Create modified recipe', key='-Modify-', disabled=True),
            ui.button('Cancel'),
        ],
    ]

    def __init__(self):
        self.view = ''
        self.window = ui.CreateWindow().create(self.title, self.layout, self.window_size)
        self.window_hidden = True

    def run_window(self):
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
            if event == '-Modify-':
                self.window['-Modify-'].update(disabled=True)
                modified_recipe = group.GroupComponentsByLocation().main(values)
                ui.popup_text('recipe is created', title='Done', default_text=modified_recipe)
            elif event == '-RECIPE_TO_PREPARE_PATH-':
                self.window['-Prepare-'].update(disabled=False)
            elif event == '-Prepare-':
                recipe_paths = prepareGroup.PrepareRecipeToGroupComponentsService().main(
                    values['-RECIPE_TO_PREPARE_PATH-'])
                self.window[self.recipe_to_update].update(value=recipe_paths['group recipe'])
                self.window[self.read_locations].update(value=recipe_paths['locations recipe'])
                location_recipe = helpers.Helpers().get_filename_from_path(recipe_paths['locations recipe']).replace(
                    '.recipe', '')
                ui.popup_text(
                    'Steps to group components:\n'
                    f'1.Open {location_recipe} recipe in cyberOptics software.\n'
                    '2.Open panel view and click on board tab.\n'
                    '3.Select first board in a boards list\n'
                    '4.Click Inspect Fids\n'
                    '5.Select Add -> Component\n'
                    '6.Draw around components you want to group\n'
                    '7.Save recipe and on save localize all parts and templates\n'
                    '8.Now you good to press OK , add suffix for components\n'
                    ' and click on Create modified recipe button \n',
                    default_text=location_recipe,
                )
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
        return prefix_from_file_name == prefix
