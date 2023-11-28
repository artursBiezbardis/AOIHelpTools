import shutil
import os
import helpers.helpers as helper
import app.services.groupComponentsByLocationService.goupComponentsByLocationService as groupComponents
import io
import app.repositories.groupComponentsByLocationRepository.recipeToUpdateRepository as updateRecipe
import helpers.compressAndExtractRecipesHelper as compressAndExtractRecipes


class PrepareRecipeToGroupComponentsRepository:

    def prepare_locations_recipe_gzip_stream(self, locations_recipe_folder_path):
        helpers = helper.Helpers()
        group_components = groupComponents.GroupComponentsByLocation()
        recipe_path = locations_recipe_folder_path
        list_of_gzip_files = group_components.prepare_recipe_data(recipe_path)
        list_of_gzip_files = self.create_copy_of_first_board(recipe_path, list_of_gzip_files)

        with open(recipe_path + '/tmp/0.board', 'rb') as f:
            gzip_stream = io.BytesIO(f.read())

        recipe_repo = updateRecipe.RecipeToUpdateRepository()
        updated_gzip_stream = recipe_repo.prepare_locations_recipe_gzip_stream(gzip_stream)

        with open(recipe_path + '/tmp/0.board', 'wb') as f_updated:
            f_updated.write(updated_gzip_stream.read())
        updated_recipe = recipe_path + '/' + helpers.get_filename_from_path(recipe_path) + '.recipe'
        compressAndExtractRecipes.CompressAndExtractRecipesHelper().compress_files_zip(updated_recipe,
                                                                                       list_of_gzip_files,
                                                                                       recipe_path + '/tmp/')

    @staticmethod
    def create_copy_of_first_board(locations_recipe_folder_path, list_of_gzip_files):
        board1_path = locations_recipe_folder_path + '/tmp/0.board'
        destination_path = locations_recipe_folder_path + '/tmp/1.board'
        if '1.board' in list_of_gzip_files:
            os.remove(destination_path)
        else:
            list_of_gzip_files.append('1.board')
        shutil.copy(board1_path, destination_path)

        return list_of_gzip_files
