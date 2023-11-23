import app.repositories.recipesListRepository.recipesListRepository as recipesList
import app.repositories.sqlLiteRepository.sqlLiteRepository as sql
import app.services.settingsService.settingsService as settings


class RecipesListService:

    dBSubLocation = '\\TemplateLibrary\\Templates.db'
    table = 'Component'
    setting_name = '-RECIPES_PATH-'


    def formatListForTable(self, entry: str, entryType: str):
        recipesFolder = settings.SettingsService().get_setting(self.setting_name)
        directories = (recipesList.RecipesListRepository()).folder_dict(recipesFolder)
        recipes_list = {}
        if entryType == 'Component':
            entryType = 'TemplateId'
        elif entryType == 'Package':
            entryType = 'PackageName'
        recipesRepository = sql.SQLiteRepository()
        for key, value in directories.items():
            recipe_path = value
            template_data_base = recipe_path + self.dBSubLocation
            if entryType == 'TemplateId':
                entry = entry.upper()
                result = recipesRepository.checkIfEnteryExist(self.table, entryType, entry, template_data_base)
            else:
                result = recipesRepository.checkIfEnteryExist(self.table, entryType, entry, template_data_base)
            package = recipesRepository.get_component_package_name(self.table, entry, template_data_base)
            if result:
                recipes_list[key] = {'location': value, 'Package': package[0]}

        return recipes_list
