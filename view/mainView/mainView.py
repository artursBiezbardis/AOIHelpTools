import createWindow as ui


class MainView:
    title = 'AOI Help Tools'
    button_cancel_title = 'Quit'
    button_settings = 'Settings'

    tools = (
        (
            'Compare Mash',
            'Diff two mash files so you can seed a new AOI recipe from an existing one.',
        ),
        (
            'Find Recipes by Part',
            'Find every recipe that uses a part, then update it from the library template.',
        ),
        (
            'Group Components',
            'Draw an area to split out components that need their own pad treatment.',
        ),
        (
            'Compare Recipe Mash',
            'See mash vs recipe part mismatches, then update the recipe from mash data.',
        ),
    )

    window_size = (640, 560)
    layout = [
        [ui.text('AOI Help Tools', heading=True)],
        [ui.text('Pick a tool. Less hunting through recipes — more boards inspected.', muted=True)],
        [ui.tool_card(name, description) for name, description in tools],
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
        tool_names = {name for name, _description in self.tools}
        while True:
            event, _values = self.window.read()
            if event is None or event == 'Quit' or event == 'Cancel':
                self.view = ''
                break
            elif event == 'Settings' or event in tool_names:
                self.view = event
                self.window.hide()
                self.window_hidden = True
                break
