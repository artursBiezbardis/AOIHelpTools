import view.mainView.mainView as MainView
import view.mashCompareView.mashCompareView as MashCompare
import view.findRecipesByPartView.findRecipesByPartView as FindRecipes
import view.settingsView.settingsView as settingsView

mainView = MainView.MainView()
mashCompareView = MashCompare.MashCompare()
findRecipes = FindRecipes.FindRecipesByPartView()
settings = settingsView.Settings()
view = 'main view'

while view:
    if view == 'main view':
        mainView.run_window()
        view = mainView.view
    elif view == 'Compare Mash':
        mashCompareView.run_window()
        view = mashCompareView.view
    elif view == 'Find Recipes by Part':
        findRecipes.run_window()
        view = findRecipes.view
    elif view == 'Settings':
        settings.run_window()
        view = settings.view