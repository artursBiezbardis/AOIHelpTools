import PySimpleGUI as sg
import createWindow as createWindow
import app.services.recipesListService.recipesListService as recipesList


class FindRecipesByPartView:
    title = 'Collect all recipes by part name or template'
    window_size = (400, 200)
    layout = [
        [
            [
                sg.Input(key='-NAME-', enable_events=True, size=(10, 1)),
                sg.Listbox(['Component', 'Package'],
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
        [sg.Multiline('', key='-RECIPES-', size=(35, 5))],
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
                if values['-NAME-']:
                    self.window['-COLLECT-'].update(disabled=False)
                else:
                    self.window['-COLLECT-'].update(disabled=True)
            elif event == '-COLLECT-':
                recipes_results = recipes.formatListForTable(values['-NAME-'], values['-SELECTION-'][0])
                self.window['-RECIPES-'].update(recipes_results)
