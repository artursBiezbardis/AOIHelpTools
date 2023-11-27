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
        elif entry_type == 'Package':
            entry_type = 'PackageName'
        recipes_repository = sql.SQLiteRepository()
        for key, value in directories.items():
            recipe_path = value
            template_data_base = recipe_path + self.dBSubLocation
            if entry_type == 'TemplateId':
                entry = entry.upper()
                result = recipes_repository.checkIfEnteryExist(self.table, entry_type, entry, template_data_base)
            else:
                result = recipes_repository.checkIfEnteryExist(self.table, entry_type, entry, template_data_base)
            package = recipes_repository.get_component_package_name(self.table, entry, template_data_base)
            if result:
                recipes_list[key] = {'location': value, 'Package': package[0]}

        return recipes_list
