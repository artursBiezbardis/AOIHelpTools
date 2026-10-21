import app.repositories.recipesListRepository.recipesListRepository as recipesList
import app.repositories.sqlLiteRepository.sqlLiteRepository as sql
import app.services.settingsService.settingsService as settings
from concurrent.futures import ThreadPoolExecutor


class RecipesListService:

    dBSubLocation = '\\TemplateLibrary\\Templates.db'
    table = 'Component'
    setting_name = '-RECIPES_PATH-'
    _max_lookup_workers = 8

    def format_list_for_table(self, entry: str, entry_type: str):
        recipes_folder = settings.SettingsService().get_setting(self.setting_name)
        directories = (recipesList.RecipesListRepository()).folder_dict(recipes_folder)
        if not directories:
            return {}

        if entry_type == 'Component':
            column = 'TemplateId'
            entry = entry.upper()
        elif entry_type == 'Package':
            column = 'PackageName'
        else:
            column = entry_type

        repository = sql.SQLiteRepository()
        table = self.table
        database_suffix = self.dBSubLocation

        def lookup(item):
            key, recipe_path = item
            found, package_name = repository.lookup_component_package(
                table,
                column,
                entry,
                recipe_path + database_suffix,
            )
            if not found:
                return None
            return key, recipe_path, package_name

        items = list(directories.items())
        if len(items) == 1:
            results = map(lookup, items)
        else:
            workers = min(self._max_lookup_workers, len(items))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                results = list(pool.map(lookup, items))

        recipes_list = {}
        for result in results:
            if result is None:
                continue
            key, recipe_path, package_name = result
            recipes_list[key] = {'location': recipe_path, 'Package': package_name}

        return recipes_list
