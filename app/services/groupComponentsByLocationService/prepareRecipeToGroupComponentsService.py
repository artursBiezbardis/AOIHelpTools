import shutil
class PrepareRecipeToGroupComponentsService:

    def main(self, recipe_path):
        # create two copies of recipe and rename them with suffixes -group and -locations in recipes folder
        # for locations recipe create additional board exactly the same as 0.board
        # remove all components from locations recipe 0.board and put recipe back

        return # -group recipe path and -locations recipe path to add paths to group recipe path and locations recipe path

    def create_process_recipes(self, recipe_path):
        locations_recipe_suffix = '-locations'
        group_recipe_suffix = '-group'
        locations_recipe_path = recipe_path + locations_recipe_suffix
        group_recipe_path = recipe_path + group_recipe_suffix
        shutil.copytree(recipe_path, locations_recipe_path)
        shutil.copytree(recipe_path, group_recipe_path)


