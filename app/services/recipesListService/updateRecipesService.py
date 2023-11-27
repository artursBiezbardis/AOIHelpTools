import helpers.compressAndExtractRecipesHelper as compressAndExtractRecipes
import helpers.helpers as help
import os
import io
import shutil
import app.repositories.recipesListRepository.updateRecipesRepository as updateRecipesRepository
from datetime import datetime


class UpdateRecipesService:

    def update_recipes(self, recipes_results, name, selection):
        # get each panel and update it part or template as Shared
        for key, value in recipes_results.items():
            recipe_folder_path = value['location']
            self.prepare_recipe_data(recipe_folder_path)
            self.set_to_shared_stream(recipe_folder_path, name, value['Package'], selection)
            shutil.rmtree(recipe_folder_path + '\\tmp')

    def set_to_shared_stream(self, recipe_path, name, package_name, selection) -> str:
        helpers = help.Helpers()
        backup_dir = 'backupRecipes'

        list_of_gzip_files = self.prepare_recipe_data(recipe_path)

        with open(recipe_path + '/tmp/Panel', 'rb') as f:
            gzip_stream = io.BytesIO(f.read())

        updated_gzip_stream = updateRecipesRepository.UpdateRecipesRepository() \
            .update_panel_gzip_stream(gzip_stream, name, package_name, selection)

        with open(recipe_path + '/tmp/Panel', 'wb') as f_updated:
            f_updated.write(updated_gzip_stream.read())

        recipe = recipe_path + '\\' + helpers.get_filename_from_path(recipe_path) + '.recipe'
        time_now = datetime.now()
        directory_list = os.listdir(recipe_path)

        if backup_dir not in directory_list:
            os.mkdir(recipe_path + f'\\{backup_dir}')

        backup_path = recipe_path + f'\\{backup_dir}\\' + time_now.strftime('%d-%m-%Y-%H_%M_%S.recipe')
        shutil.move(recipe, backup_path)
        compressAndExtractRecipes.CompressAndExtractRecipesHelper().compress_files_zip(recipe,
                                                                                       list_of_gzip_files,
                                                                                       recipe_path + '/tmp/')
        return helpers.get_filename_from_path(recipe).replace('.recipe', '')

    @staticmethod
    def prepare_recipe_data(path_to_recipe):
        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()
        file_name = helpers.get_filename_from_path(path_to_recipe) + '.recipe'
        extract_recipe.extract_zip(path_to_recipe, file_name)
        list_of_gzip_files = helpers.get_files_in_folder(path_to_recipe + '/tmp')

        return list_of_gzip_files
