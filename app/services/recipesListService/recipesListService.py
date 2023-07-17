import app.repositories.recipesListRepository.recipesListRepository as recipesList
import app.repositories.sqlLiteRepository.sqlLiteRepository as sql


class RecipesListService:

    def formatListForTable(self, entry: str, entryType: str) -> list:
        directories = (recipesList.RecipesListRepository()).folder_dict(
            "C:\\Users\\arturs.biezbardis\\Desktop\\testFolder\\Recipes")
        for key, value in directories.items():
            print(f"Folder: {key}, Location: {value}")

        #return entry
