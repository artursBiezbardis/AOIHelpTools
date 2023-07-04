import view.mainView.mainView as MainView
import view.mashCompareView.mashCompareView as MashCompare

mainView = MainView.MainView()
mashCompareView = MashCompare.MashCompare()
view = 'main view'

while view:
    test = "test"
    if view == 'main view':
        mainView.run_window()
        view = mainView.view
    elif view == 'Compare Mash':
        mashCompareView.run_window()
        view = mashCompareView.view