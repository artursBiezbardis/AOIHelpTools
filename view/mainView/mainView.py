import createWindow as ui


class MainView:
    title = 'AOI Help Tools'
    button1_title = 'Compare Mash'
    button_cancel_title = 'Cancel'
    button2_title = 'Find Recipes by Part'
    button_settings = 'Settings'
    button_group_components = 'Group Components'
    button_compare_recipe_mash = 'Compare Recipe Mash'

    window_size = (760, 120)
    layout = [
        [
            ui.button(button1_title),
            ui.button(button2_title),
            ui.button(button_group_components),
            ui.button(button_compare_recipe_mash),
        ],
        [
            ui.button(button_settings),
            ui.button(button_cancel_title),
        ],
    ]

    def __init__(self):
        self.view = ''
        self.window = ui.CreateWindow().create(self.title, self.layout, self.window_size)
        self.window_hidden = True

    def run_window(self):
        self.window.un_hide()
        self.window_hidden = False
        while True:
            event, _values = self.window.read()
            if event is None or event == 'Cancel':
                self.view = ''
                break
            elif event in (
                'Compare Mash',
                'Find Recipes by Part',
                'Settings',
                'Group Components',
                'Compare Recipe Mash',
            ):
                self.view = event
                self.window.hide()
                self.window_hidden = True
                break
