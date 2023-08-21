import PySimpleGUI as sg
from view import createWindow as createWindow
import app.repositories.sqlLiteRepository.sqlLiteSettingsRepository as settingsRepository


class Settings:

    title = 'Settings'
    window_size = (1200, 500)
    recipes_folder_default = settingsRepository.Settings().get_setting_value('recipes_folder')
    excel_export_folder_default = '2'
    layout = [
        [
            [
                sg.Text('Select recipes folder  '),
                sg.Input(recipes_folder_default, key='-RECIPES_FOLDER-', enable_events=True),
                sg.FolderBrowse('select folder')
            ],
            [
                sg.Text('Mash compare Excel export location  '),
                sg.Input(excel_export_folder_default, key='-EXCEL_EXPORT_FOLDER-', enable_events=True),
                sg.FolderBrowse('select folder')
            ]
        ],
        [
            sg.B('Update settings', key='-UPDATE-', disabled=True, enable_events=True),
            sg.Button('Cancel')

        ],
        []

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
