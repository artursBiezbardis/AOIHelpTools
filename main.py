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
        test = "test"
    elif view == 'Compare Mash':
        while view == 'Compare Mash':
            if view == 'Compare Mash':
                mashCompareView.run_window()
