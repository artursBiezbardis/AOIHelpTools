import app.repositories.recipesListRepository.recipesListRepository as recipesList
import app.repositories.sqlLiteRepository.sqlLiteRepository as sql


class RecipesListService:

    dBSubLocation = '\\TemplateLibrary\\Templates.db'
    table = 'Component'
    recipesFolder = "Z:\\Recipe"

    def formatListForTable(self, entry: str, entryType: str):
        directories = (recipesList.RecipesListRepository()).folder_dict(self.recipesFolder)
        entryRecipes = ''
        if entryType == 'Component':
            entryType = 'TemplateId'
        elif entryType == 'Package':
            entryType = 'PackageName'
        recipesRepository = sql.SQLiteRepository()
        for key, value in directories.items():
            if entryType == 'TemplateId':
                entry = entry.upper()
                result = recipesRepository.checkIfEnteryExist(self.table, entryType, entry, value+self.dBSubLocation)
            else:
                result = recipesRepository.checkIfEnteryExist(self.table, entryType, entry, value + self.dBSubLocation)

            if result:
                entryRecipes += key+'\n'

        return entryRecipes