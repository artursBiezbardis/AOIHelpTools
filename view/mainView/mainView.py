import createWindow as createWindow
import PySimpleGUI as sg


class MainView:
    title: str = 'main view'
    button1_title: str = 'Compare Mash'
    button_cancel_title: str = 'Cancel'
    button2_title: str = 'Find Recipes by Part'
    button_settings: str = 'Settings'
    button_group_components: str = 'Group Components'
    button_compare_recipe_mash: str = 'Compare Recipe Mash'

    window_size = (600, 80)
    layout: [[sg.Button]] = [[
        sg.Button(button1_title),
        sg.Button(button2_title),
        sg.Button(button_group_components),
        sg.Button(button_compare_recipe_mash),
    ], [
        sg.Button(button_settings),
        sg.Button(button_cancel_title)
    ]]

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

        while True:

            if self.window_hidden:
                self.window.un_hide()
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                self.view = ''

                break

            elif event == 'Compare Mash':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break

            elif event == 'Find Recipes by Part':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break


            elif event == 'Settings':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break

            elif event == 'Group Components':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break

            elif event == 'Compare Recipe Mash':

                self.view = event
                self.window.hide()
                self.window_hidden = True
                break

            self.window.close()


