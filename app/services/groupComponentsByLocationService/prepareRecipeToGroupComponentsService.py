import shutil
import os
import helpers.helpers as helper
import app.services.groupComponentsByLocationService.goupComponentsByLocationService as groupComponents
import io
import app.repositories.groupComponentsByLocationRepository.recipeToUpdateRepository as updateRecipe
import helpers.compressAndExtractRecipesHelper as compressAndExtractRecipes


class PrepareRecipeToGroupComponentsService:

    def main(self, recipe_path):
        return self.create_process_recipes(recipe_path)

    def create_process_recipes(self, recipe_path: str) -> object:
        locations_recipe_suffix = '-locations'
        group_recipe_suffix = '-group'
        locations_recipe_folder_path = recipe_path + locations_recipe_suffix
        group_recipe_folder_path = recipe_path + group_recipe_suffix
        shutil.copytree(recipe_path, locations_recipe_folder_path)
        shutil.copytree(recipe_path, group_recipe_folder_path)
        old_recipe_name = helper.Helpers().get_filename_from_path(recipe_path)
        locations_recipe_name = helper.Helpers().get_filename_from_path(locations_recipe_folder_path)
        group_recipe_name = helper.Helpers().get_filename_from_path(group_recipe_folder_path)
        locations_recipe_path = recipe_path + locations_recipe_suffix + '/' + locations_recipe_name + '.recipe'
        group_recipe_path = recipe_path + group_recipe_suffix + '/' + group_recipe_name + '.recipe'
        os.rename(recipe_path + locations_recipe_suffix + '/' + old_recipe_name + '.recipe', locations_recipe_path)
        os.rename(recipe_path + group_recipe_suffix + '/' + old_recipe_name + '.recipe', group_recipe_path)

        self.prepare_locations_recipe_gzip_stream(locations_recipe_folder_path)
        process_recipes_path = {'locations recipe': locations_recipe_folder_path,
                                'group recipe': group_recipe_folder_path
                                }
        shutil.rmtree(locations_recipe_folder_path + '/tmp/')

        return process_recipes_path

    def prepare_locations_recipe_gzip_stream(self, locations_recipe_folder_path):
        helpers = helper.Helpers()
        group_components = groupComponents.GroupComponentsByLocation()
        recipe_path = locations_recipe_folder_path
        list_of_gzip_files = group_components.prepare_recipe_data(recipe_path)
        self.create_copy_of_first_board(recipe_path)
        list_of_gzip_files.append('1.board')

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
    def create_copy_of_first_board(locations_recipe_folder_path):
        board1_path = locations_recipe_folder_path + '/tmp/0.board'
        destination_path = locations_recipe_folder_path + '/tmp/1.board'
        shutil.copy(board1_path, destination_path)
