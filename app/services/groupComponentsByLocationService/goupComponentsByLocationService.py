import zipfile
import app.models.LocationsCollection as areaLocationCollection
import helpers.compressAndExtractRecipesHelper as compressAndExtractRecipes
import helpers.helpers as help
import os
import app.repositories.groupComponentsByLocationRepository.areaLocationRepository as areaLocation
import app.repositories.groupComponentsByLocationRepository.recipeToUpdateRepository as updateRecipe
import io


class GroupComponentsByLocation:

    def main(self, view_input):

        area_location_collection = self.read_area_location_data(view_input)
        self.update_component_in_recipe_gzip_stream(area_location_collection, view_input)

    def read_area_location_data(self, view_input) -> areaLocationCollection.LocationsData([]):
        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()

        recipe_path = view_input['-RECIPE_FOLDER_FOR_LOCATIONS_PATH-']
        list_of_gzip_files = self.prepare_recipe_data(recipe_path)

        # list of recipe files extracted from recipe file

        for file in list_of_gzip_files:
            if helpers.has_extension(file, '.board'):
                gzip_out_name = os.path.splitext(file)[0]
                extract_recipe.extract_gzip(recipe_path + '/tmp/',
                                            file,
                                            '/boardsXML/' + gzip_out_name)

                xml_file = recipe_path + '/tmp/boardsXML/' + gzip_out_name
                data_for_area_locations = areaLocation.AreaLocationRepository(). \
                    get_area_location_data(xml_file, view_input).areaLocationCollection

                return data_for_area_locations

    def update_component_in_recipe_gzip_stream(self, area_locations_collection, view_input):
        helpers = help.Helpers()
        recipe_path = view_input['-RECIPE_FOLDER_TO_UPDATE_PATH-']
        list_of_gzip_files = self.prepare_recipe_data(recipe_path)

        for file in list_of_gzip_files:
            if helpers.has_extension(file, '.board'):
                with open(recipe_path + '/tmp/' + file, 'rb') as f:
                    gzip_stream = io.BytesIO(f.read())

                recipe_repo = updateRecipe.RecipeToUpdateRepository()
                updated_gzip_stream = recipe_repo.update_board_components_in_selected_areas_gzip_stream(
                    gzip_stream,
                    area_locations_collection,
                    view_input['-SUFFIX-']
                )

                with open(recipe_path + '/tmp/' + file, 'wb') as f_updated:
                    f_updated.write(updated_gzip_stream.read())

                # edit recipe gzip hex to pass stream when opening recipe in cyberOptics AOI software
                help.Helpers().edit_hex_in_file(recipe_path + '/tmp/' + file, 0, '1F8B0800000000000400')

        updated_recipe = recipe_path + '/' + help.Helpers().get_filename_from_path(recipe_path) + '_grouped.recipe'

        compressAndExtractRecipes.CompressAndExtractRecipesHelper().compress_files_zip(updated_recipe,
                                                                                       list_of_gzip_files,
                                                                                       recipe_path + '/tmp/')

    @staticmethod
    def prepare_recipe_data(path_to_recipe):

        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()
        file_name = helpers.get_filename_from_path(path_to_recipe) + '.recipe'
        extract_recipe.extract_zip(path_to_recipe, file_name)
        list_of_gzip_files = helpers.get_files_in_folder(path_to_recipe + '/tmp')
        os.mkdir(path_to_recipe + '/tmp/boardsXML')

        return list_of_gzip_files
