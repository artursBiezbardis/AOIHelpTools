import PySimpleGUI as sg
import createWindow as createWindow



class Settings:
    title = 'Settings'
    window_size = (1200, 500)
    recipes_folder = 'xxxx'
    mash_compare_excel_export_folder = 'xxxx'

    layout = [
        [
            [
                sg.Input(recipes_folder, key='-Recipes-', enable_events=True),
                sg.FolderBrowse()
            ],
            [
                sg.Input(mash_compare_excel_export_folder, key='-FILE2-', enable_events=True),
                sg.FolderBrowse()
            ]
        ],
        [
            sg.B('Update settings', key='-Update-', disabled=True, enable_events=True),
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
                self.view = 'Settings'
                self.window.hide()
                self.window_hidden = True
                break

