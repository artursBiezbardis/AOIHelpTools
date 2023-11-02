import app.models.LocationsCollection as areaLocationCollection
import helpers.compressAndExtractRecipesHelper as compressAndExtractRecipes
import helpers.helpers as help
import os
import app.repositories.groupComponentsByLocationRepository.areaLocationRepository as areaLocation
import app.repositories.groupComponentsByLocationRepository.recipeToUpdateRepository as updateRecipe


class GroupComponentsByLocation:

    def main(self, view_input):

        area_location_collection = self.read_area_location_data(view_input)
        self.update_component_in_recipe(area_location_collection, view_input)

    def read_area_location_data(self, view_input) -> areaLocationCollection.LocationsData([]):
        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()

        recipe_path = view_input['-RECIPE_FOLDER_FOR_LOCATIONS_PATH-']
        list_of_gzip_files = self.prepare_recipe_data(recipe_path)

        # list of recipe files extracted from recipe file

        for file in list_of_gzip_files:
            if helpers.has_extension(file, '.board'):
                gzip_out_name = os.path.splitext(file)[0]
                extract_recipe.extract_compress_gzip(helpers.correct_path_string(recipe_path), file,
                                                     '\\tmp\\boardsXML\\' + gzip_out_name)

                xml_file = recipe_path + '\\tmp\\boardsXML\\' + gzip_out_name

                data_for_area_locations = areaLocation.AreaLocationRepository(). \
                    get_area_location_data(xml_file, view_input).areaLocationCollection

                for item in data_for_area_locations:
                    val = item.check_contains_component(72.0996208190918, 80.30043029785156)
                    print(val)
                return data_for_area_locations

    def update_component_in_recipe(self, area_locations_collection, view_input):
        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()
        recipe_path = view_input['-RECIPE_FOLDER_TO_UPDATE_PATH-']
        list_of_gzip_files = self.prepare_recipe_data(recipe_path)

        for file in list_of_gzip_files:
            if helpers.has_extension(file, '.board'):
                gzip_out_name = os.path.splitext(file)[0]
                extract_recipe.extract_compress_gzip(helpers.correct_path_string(recipe_path), file,
                                                     '\\tmp\\boardsXML\\' + gzip_out_name)

                xml_file = recipe_path + '\\tmp\\boardsXML\\' + gzip_out_name

                updateRecipe.RecipeToUpdateRepository().update_board_components_in_selected_areas(xml_file, area_locations_collection, view_input['-SUFFIX-'])



    @staticmethod
    def prepare_recipe_data(path_to_recipe):

        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()

        file_name = helpers.get_filename_from_path(path_to_recipe) + '.recipe'
        extract_recipe.extract_zip(path_to_recipe, file_name)
        list_of_gzip_files = helpers.get_files_in_folder(path_to_recipe + '\\tmp')
        os.mkdir(path_to_recipe + '\\tmp\\boardsXML')

        return list_of_gzip_files

