import PySimpleGUI as sg
import createWindow as createWindow


class FindRecipesByPartView:
    title = 'Collect all recipes by part name or template'
    layout = [
        [
            [
                sg.Input(key='-NAME-', enable_events=True),
                sg.Listbox(['Part', 'Template'], select_mode=True, enable_events=True, default_values=['Part'])],
        ],
        [sg.B('Collect', disabled=True), sg.Button('Cancel')]
    ]

    def __init__(self):
        self.view = ''
        self.window = createWindow.CreateWindow.create(self.title, self.layout)
        self.window_hidden = False

    def run_window(self):
        if self.window_hidden:
            self.window.un_hide()

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                self.window.close()
                break
            elif event == 'Cancel':
                self.view = 'main view'
                self.window.hide()
                self.window_hidden = True
                break
            elif event[1] != '':
                print(values['-NAME-'], self.layout)
                for row in self.layout:
                    for element in row:
                        test = element
                        #element.update(visible=False)
                    # Show the new part of the layout
                #window['-COL-'].update(visible=True)

            print('You entered ', values[0], values['-NAME-'])
