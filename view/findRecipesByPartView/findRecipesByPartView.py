import createWindow as ui
import app.services.recipesListService.recipesListService as recipesList
import app.services.recipesListService.updateRecipesService as updateRecipesService


class FindRecipesByPartView:
    title = 'Collect all recipes by part name or template'
    window_size = (640, 280)
    layout = [
        [
            ui.input_box('-NAME-', enable_events=True, width=18),
            ui.listbox('-SELECTION-', ['Component'], default=['Component']),
        ],
        [
            ui.button('Collect', key='-COLLECT-', disabled=True),
            ui.button('Cancel'),
        ],
        [ui.multiline('-RECIPES-', height=8, width=70)],
        [ui.button('Update part in all recipes', key='-UPDATE_RECIPES-', disabled=True)],
    ]

    def __init__(self):
        self.view = ''
        self.window = ui.CreateWindow().create(self.title, self.layout, self.window_size)
        self.window_hidden = True

    def run_window(self):
        recipes = recipesList.RecipesListService()
        update_recipes = updateRecipesService.UpdateRecipesService()
        recipes_results = {}
        part_name = ''
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
            if event == '-NAME-':
                part_name = values['-NAME-'].upper()
                self.window['-COLLECT-'].update(disabled=part_name == '')
            elif event == '-COLLECT-':
                recipes_text_list = ''
                recipes_results = recipes.format_list_for_table(part_name, values['-SELECTION-'][0])
                for key, value in recipes_results.items():
                    recipes_text_list += key + '  Package:' + value['Package'] + '\n'
                self.window['-RECIPES-'].update(value=recipes_text_list)
                self.window['-UPDATE_RECIPES-'].update(disabled=False)
            elif event == '-UPDATE_RECIPES-':
                update_recipes.update_recipes(recipes_results, part_name, values['-SELECTION-'][0])
