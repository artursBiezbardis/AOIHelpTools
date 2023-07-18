import app.repositories.recipesListRepository.recipesListRepository as recipesList
import app.repositories.sqlLiteRepository.sqlLiteRepository as sql


class RecipesListService:
    dBSubLocation = '\\TemplateLibrary\\Templates.db'
    def formatListForTable(self, entry: str, entryType: str) -> list:
        directories = (recipesList.RecipesListRepository()).folder_dict(
            "C:\\Users\\arturs.biezbardis\\Desktop\\testFolder\\Recipes")
        entryRecipes = []
        recipesRepository = sql.SQLiteRepository()
        for key, value in directories.items():
            #recipesRepository.connectToDB(value+self.dBSubLocation)
            print(f"Folder: {key}, Location: {value}")

        #return entry
