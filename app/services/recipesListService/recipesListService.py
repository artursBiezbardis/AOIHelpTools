import app.repositories.recipesListRepository.recipesListRepository as recipesList
import app.repositories.sqlLiteRepository.sqlLiteRepository as sql
import app.services.settingsService.settingsService as settings


class RecipesListService:

    dBSubLocation = '\\TemplateLibrary\\Templates.db'
    table = 'Component'
    setting_name = '-RECIPES_PATH-'

    def format_list_for_table(self, entry: str, entry_type: str):
        recipes_folder = settings.SettingsService().get_setting(self.setting_name)
        directories = (recipesList.RecipesListRepository()).folder_dict(recipes_folder)
        recipes_list = {}
        if entry_type == 'Component':
            entry_type = 'TemplateId'
            entry = entry.upper()
        elif entry_type == 'Package':
            entry_type = 'PackageName'
        recipes_repository = sql.SQLiteRepository()
        for key, value in directories.items():
            template_data_base = value + self.dBSubLocation
            result, package = recipes_repository.lookup_recipe_component(
                self.table, entry_type, entry, template_data_base)
            if result:
                recipes_list[key] = {'location': value, 'Package': package[0]}

        return recipes_list
