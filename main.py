import view.mainView.mainView as MainView
import view.mashCompareView.mashCompareView as MashCompare
import PySimpleGUI as sg

mainView = MainView.MainView()
mashCompareView = MashCompare.MashCompare()
view = 'main view'

while view:
    if view == 'main view':
        mainView.run_window()
        view = mainView.view
    elif view == 'Compare Mash':
        mashCompareView.run_window()
        view = mashCompareView.view

