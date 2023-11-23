import PySimpleGUI as sg
import createWindow as createWindow
import app.services.recipesListService.recipesListService as recipesList
import app.services.recipesListService.updateRecipesService as updateRecipesService


class FindRecipesByPartView:
    title = 'Collect all recipes by part name or template'
    window_size = (400, 200)
    layout = [
        [
            [
                sg.Input(key='-NAME-', enable_events=True, size=(10, 1)),
                sg.Listbox(['Component'],
                           key='-SELECTION-',
                           select_mode=True,
                           enable_events=True,
                           default_values=['Component'],
                           size=(10, 2),
                           )
            ],
        ],
        [
            sg.B('Collect', disabled=True, key='-COLLECT-'),
            sg.Button('Cancel')
         ],
        [sg.Multiline('', key='-RECIPES-', size=(60, 5))],
        [sg.B('Update part in all recipes', disabled=True, key='-UPDATE_RECIPES-')]
    ]

    def __init__(self):
        self.view = ''
        self.window = createWindow.CreateWindow.create(
            createWindow.CreateWindow(),
            self.title,
            self.layout,
            self.window_size
        )
        self.window_hidden = False

    def run_window(self):
        recipes = recipesList.RecipesListService()
        update_recipes = updateRecipesService.UpdateRecipesService()
        recipes_text_list = ''
        recipes_results = {}
        part_name = ''
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
            elif event == '-NAME-':
                part_name = values['-NAME-'].upper()
                if part_name != '':
                    self.window['-COLLECT-'].update(disabled=False)
                else:
                    self.window['-COLLECT-'].update(disabled=True)
            elif event == '-COLLECT-':
                recipes_text_list = ''
                recipes_results = recipes.formatListForTable(part_name, values['-SELECTION-'][0])
                for key, value in recipes_results.items():

                    recipes_text_list += key + '  Package:' + value['Package'] + '\n'

                self.window['-RECIPES-'].update(recipes_text_list)
                self.window['-UPDATE_RECIPES-'].update(disabled=False)

            elif event == '-UPDATE_RECIPES-':

                update_recipes.update_recipes(recipes_results, part_name, values['-SELECTION-'][0])