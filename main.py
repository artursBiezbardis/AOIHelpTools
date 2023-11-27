import view.mainView.mainView as MainView
import view.mashCompareView.mashCompareView as MashCompare
import view.findRecipesByPartView.findRecipesByPartView as FindRecipes
import view.settingsView.settingsView as settingsView
import view.groupComponentsByLocationView.groupComponentsByLocationView as GroupComponents

main_view = MainView.MainView()
mash_compare_view = MashCompare.MashCompare()
find_recipes = FindRecipes.FindRecipesByPartView()
settings = settingsView.Settings()
group_components = GroupComponents.GroupComponents()


view = 'main view'

while view:
    if view == 'main view':
        main_view.run_window()
        view = main_view.view
    elif view == 'Compare Mash':
        mash_compare_view.run_window()
        view = mash_compare_view.view
    elif view == 'Find Recipes by Part':
        find_recipes.run_window()
        view = find_recipes.view
    elif view == 'Settings':
        settings.run_window()
        view = settings.view
    elif view == 'Group Components':
        group_components.run_window()
        view = group_components.view
