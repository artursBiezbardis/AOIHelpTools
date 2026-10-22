import helpers.helpers as helper
import os
import utilities.compressExtractZipUtilities as zipUtilities


class RecipeProcessUtilities:

    def prepare_tmp_recipe_data(self, path_to_recipe):
        helpers = helper.Helpers()
        extract_recipe = zipUtilities.CompressExtractZipUtilities()
        extract_folder_path = os.path.dirname(path_to_recipe) + '/tmp'
        self.create_directory(extract_folder_path)
        extract_recipe.extract_zip(path_to_recipe, extract_folder_path)
        list_of_gzip_files = helpers.get_files_in_folder(extract_folder_path)

        return {'gzip_list': list_of_gzip_files, 'gzip_extract_path': extract_folder_path}

    @staticmethod
    def create_recipe_from_tmp(path_to_recipe, list_of_gzip_files):
        tmp_folder_path = os.path.dirname(path_to_recipe) + '/tmp'
        zipUtilities.CompressExtractZipUtilities().compress_zip_files(path_to_recipe,
                                                                      list_of_gzip_files,
                                                                      tmp_folder_path)

    @staticmethod
    def create_directory(dir_path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
