import view.mainView.mainView as MainView
import view.mashCompareView.mashCompareView as MashCompare
import view.findRecipesByPartView.findRecipesByPartView as FindRecipes
import view.settingsView.settingsView as settingsView
import view.groupComponentsByLocationView.groupComponentsByLocationView as GroupComponents

mainView = MainView.MainView()
mashCompareView = MashCompare.MashCompare()
findRecipes = FindRecipes.FindRecipesByPartView()
settings = settingsView.Settings()
groupComponents = GroupComponents.GroupComponents()


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
    elif view == 'Group Components':
        groupComponents.run_window()
        view = groupComponents.view
