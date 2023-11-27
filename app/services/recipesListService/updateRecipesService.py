import helpers.compressAndExtractRecipesHelper as compressAndExtractRecipes
import helpers.helpers as help
import os
import shutil
import app.repositories.recipesListRepository.updateRecipesRepository as updateRecipesRepository
from datetime import datetime


class UpdateRecipesService:

    def update_recipes(self, recipes_results, part_name, selection):
        for key, value in recipes_results.items():
            recipe_folder_path = value['location']
            self.prepare_recipe_data(recipe_folder_path)
            self.set_to_shared_stream(recipe_folder_path, part_name, value['Package'], selection)
            shutil.rmtree(recipe_folder_path + '\\tmp')

    def set_to_shared_stream(self, recipe_path, part_name, package_name, selection) -> str:
        helpers = help.Helpers()
        backup_dir_name = 'backupRecipes'

        list_of_gzip_files = self.prepare_recipe_data(recipe_path)
        updateRecipesRepository.UpdateRecipesRepository().stream_gzip_for_update(part_name, package_name, recipe_path)
        recipe_file_path = recipe_path + '\\' + helpers.get_filename_from_path(recipe_path) + '.recipe'
        self.create_backup_for_file(recipe_path, backup_dir_name, recipe_file_path)
        compressAndExtractRecipes.CompressAndExtractRecipesHelper().compress_files_zip(recipe_file_path,
                                                                                       list_of_gzip_files,
                                                                                       recipe_path + '/tmp/')
        return helpers.get_filename_from_path(recipe_file_path).replace('.recipe', '')

    @staticmethod
    def prepare_recipe_data(path_to_recipe):
        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()
        file_name = helpers.get_filename_from_path(path_to_recipe) + '.recipe'
        extract_recipe.extract_zip(path_to_recipe, file_name)
        list_of_gzip_files = helpers.get_files_in_folder(path_to_recipe + '/tmp')

        return list_of_gzip_files

    @staticmethod
    def create_backup_for_file(dir_path, backup_dir, file_path):
        time_now = datetime.now()
        directory_list = os.listdir(dir_path)
        if backup_dir not in directory_list:
            os.mkdir(dir_path + f'\\{backup_dir}')
        backup_path = dir_path + f'\\{backup_dir}\\' + time_now.strftime('%d-%m-%Y-%H_%M_%S.recipe')
        shutil.move(file_path, backup_path)
