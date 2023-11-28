import shutil
import os
import helpers.helpers as helper
import app.repositories.groupComponentsByLocationRepository.prepareRecipeToGroupComponentsRepository as prepareRecipe


class PrepareRecipeToGroupComponentsService:

    def main(self, recipe_path):

        return self.create_data_process_recipes(recipe_path)

    @staticmethod
    def create_data_process_recipes(recipe_path: str) -> object:

        prepare_recipe_repo = prepareRecipe.PrepareRecipeToGroupComponentsRepository()
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
        prepare_recipe_repo.prepare_locations_recipe_gzip_stream(locations_recipe_folder_path)
        process_recipes_path = {'locations recipe': locations_recipe_folder_path,
                                'group recipe': group_recipe_folder_path}
        shutil.rmtree(locations_recipe_folder_path + '/tmp/')

        return process_recipes_path
