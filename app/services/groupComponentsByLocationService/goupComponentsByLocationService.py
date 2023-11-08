import zipfile
import app.models.LocationsCollection as areaLocationCollection
import helpers.compressAndExtractRecipesHelper as compressAndExtractRecipes
import helpers.helpers as help
import os
import app.repositories.groupComponentsByLocationRepository.areaLocationRepository as areaLocation
import app.repositories.groupComponentsByLocationRepository.recipeToUpdateRepository as updateRecipe
import shutil
import chardet
import gzip
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
                #os.mkdir(recipe_path + '/tmp/boardsXML')
                extract_recipe.extract_gzip(recipe_path + '/tmp/', file,
                                                     '/boardsXML/' + gzip_out_name)

                #xml_file = helpers.correct_path_string(recipe_path + '/tmp/boardsXML/' + gzip_out_name)
                xml_file = recipe_path + '/tmp/boardsXML/' + gzip_out_name

                data_for_area_locations = areaLocation.AreaLocationRepository(). \
                    get_area_location_data(xml_file, view_input).areaLocationCollection

                # for item in data_for_area_locations:
                #     val = item.check_contains_component(72.0996208190918, 80.30043029785156)
                #     print(val)
                return data_for_area_locations

    def update_component_in_recipe(self, area_locations_collection, view_input):
        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()
        recipe_path = view_input['-RECIPE_FOLDER_TO_UPDATE_PATH-']
        list_of_gzip_files = self.prepare_recipe_data(recipe_path)

        for file in list_of_gzip_files:
            if helpers.has_extension(file, '.board'):
                gzip_out_name = os.path.splitext(file)[0]
#                extract_recipe.extract_compress_gzip(helpers.correct_path_string(recipe_path), file,
#                                                     helpers.correct_path_string('/tmp/boardsXML/') + gzip_out_name)
                extract_recipe.extract_gzip(recipe_path + '/tmp/', file,
                                                     '/boardsXML/' + gzip_out_name)
#                xml_file = recipe_path + helpers.correct_path_string('/tmp/boardsXML/') + gzip_out_name
                xml_file = recipe_path + '/tmp/boardsXML/' + gzip_out_name

                updateRecipe.RecipeToUpdateRepository().update_board_components_in_selected_areas(xml_file, area_locations_collection, view_input['-SUFFIX-'])

                try:

                    os.remove(recipe_path + '/tmp/' + file)
                    print(f'File "{file}" has been successfully deleted.')
                except OSError as e:
                    print(f'Error: {e.filename} - {e.strerror}.')
                extract_recipe.compress_gzip(recipe_path + '/tmp/boardsXML/', gzip_out_name, recipe_path + '/tmp/' + file)

                self.recompress_gzip(recipe_path + '/tmp/' + file, recipe_path + '/tmp/' + file)
                try:
                    directory_path = recipe_path + '/tmp/boardsXML/'
                    os.remove(directory_path + '0')
                    shutil.rmtree(directory_path)
                    print(f'File "{directory_path}" has been successfully deleted.')
                except OSError as e:
                    print(f'Error: {e.filename} - {e.strerror}.')
                #extract_recipe.compress_zip(recipe_path, recipe_path + '/tmp/')
        zipfile_name = recipe_path + '/test.recipe'

        with zipfile.ZipFile(zipfile_name, 'w') as zipf:
            for file in list_of_gzip_files:
                zipf.write(recipe_path + '/tmp/' + file)

    def update_component_in_recipe_gzip_stream(self, area_locations_collection, view_input):
        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()
        recipe_path = view_input['-RECIPE_FOLDER_TO_UPDATE_PATH-']
        list_of_gzip_files = self.prepare_recipe_data(recipe_path)

        for file in list_of_gzip_files:


            if helpers.has_extension(file, '.board'):
                # Instead of extracting the file to disk, create a stream
                with open(recipe_path + '/tmp/' + file, 'rb') as f:
                    gzip_stream = io.BytesIO(f.read())

                # ... process the xml_content as needed ...
                # This is where you would integrate the XML processing and update logic
                # For example, parse the XML, update it with area_locations_collection data, etc.
                recipe_repo = updateRecipe.RecipeToUpdateRepository()
                updated_gzip_stream = recipe_repo.update_board_components_in_selected_areas_gzip_stream(
                    gzip_stream,
                    area_locations_collection,
                    view_input['-SUFFIX-']
                )
                # After processing the xml_content, write it back to a gzip stream

                with open(recipe_path + '/tmp/' + file, 'wb') as f_updated:
                    f_updated.write(updated_gzip_stream.read())

                help.Helpers().edit_hex_in_file(recipe_path + '/tmp/' + file, 0, '1F8B0800000000000400')
        zipfile_name = recipe_path + '/' + help.Helpers().get_filename_from_path(recipe_path) + '_grouped.recipe'

        with zipfile.ZipFile(zipfile_name, 'w') as zipf:
            for gzip_file in list_of_gzip_files:
                zipf.write(recipe_path + '/tmp/' + gzip_file, gzip_file)




    @staticmethod
    def prepare_recipe_data(path_to_recipe):

        helpers = help.Helpers()
        extract_recipe = compressAndExtractRecipes.CompressAndExtractRecipesHelper()

        file_name = helpers.get_filename_from_path(path_to_recipe) + '.recipe'
        extract_recipe.extract_zip(path_to_recipe, file_name)
        list_of_gzip_files = helpers.get_files_in_folder(path_to_recipe + '/tmp')
        os.mkdir(path_to_recipe + '/tmp/boardsXML')

        return list_of_gzip_files

    @staticmethod
    def recompress_gzip(input_gzip_path, output_gzip_path):
        # Read the contents of the input gzip file
        with open(input_gzip_path, 'rb') as f:
            compressed_data = f.read()
        os.remove(input_gzip_path)

        # Create a BytesIO stream to hold the decompressed data
        decompressed_stream = io.BytesIO(compressed_data)

        # Create a gzip decompressor object
        with gzip.GzipFile(fileobj=decompressed_stream, mode='rb') as gz:
            decompressed_data = gz.read()

        # Create a new BytesIO stream to hold the recompressed data
        recompressed_stream = io.BytesIO()

        # Create a gzip compressor object
        with gzip.GzipFile(fileobj=recompressed_stream, mode='wb') as gz:
            gz.write(decompressed_data)

        # Reset the recompressed stream position to the beginning for writing
        recompressed_stream.seek(0)

        # Save the recompressed data to a new gzip file
        with open(output_gzip_path, 'wb') as f:
            f.write(recompressed_stream.read())

