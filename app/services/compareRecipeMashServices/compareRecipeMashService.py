import app.services.groupComponentsByLocationService.goupComponentsByLocationService as prepareRecipe
import app.services.mashFileServices.mashFileService as mashService
import re
import helpers.helpers as helper
import shutil
import json
import xmltodict
import io
import gzip


class CompareRecipeMashService:

    def main(self, recipe_path, mash_path):

        prepare_recipe = prepareRecipe.GroupComponentsByLocation()

        recipe_folder_path = self.parse_recipe_folder_path(recipe_path)
        mash_service = mashService.MashFileService()
        board_side = self.pcb_side(recipe_path)
        mash_data = mash_service.extract_mash_data(mash_path)
        board_side_mash_data = self.get_board_side_data(mash_data, board_side)
        prepare_recipe.prepare_recipe_data(recipe_folder_path)
        table = self.compare_recipe_to_mash(recipe_folder_path, board_side_mash_data)

        return table

    @staticmethod
    def get_list_of_components_from_mashes(comp_name_list1, comp_name_list2):

        comp_name_list1.extend(comp_name_list2)
        comp_name_list = list(set(comp_name_list1))
        comp_name_list.sort()
        return comp_name_list

    @staticmethod
    def is_valid_component_name(name):
        try:
            return re.fullmatch(r'[a-zA-Z]+\d{1,7}', name) is not None
        except TypeError:
            return False

    @staticmethod
    def locate_diff_in_row(row, mash_data1, mash_data2):

        diff1 = []
        diff2 = []
        diff1.append(row)
        for i, (item1, item2) in enumerate(zip(mash_data1, mash_data2)):
            if item1 != item2:
                diff1.append(i)

        for item in diff1:
            diff2.append(item)
        diff2[0] = row + 1

        return [diff1, diff2]

    @staticmethod
    def format_data_content(item):

        for key, value in enumerate(item):
            if not isinstance(value, (int, float, complex)):

                item[key] = value.replace(",", ".")

                if not helper.Helpers().is_number(item[key]):
                    item[key] = value.upper()
                if helper.Helpers().is_number(item[key]):
                    item[key] = float(item[key])
                if not helper.Helpers().is_number(item[key]):
                    item[key] = helper.Helpers().replace_special_letters(item[key])
        return item

    @staticmethod
    def convert_to_list_mash_columns_not_to_compare(mash_values_not_compared):
        list_value = {
            '-PART_NUMBER-': 1,
            '-DESCRIPTION-': 2,
            '-X_CORD-': 3,
            '-Y_CORD-': 4,
            '-ROTATION-': 5,
            '-SIDE-': 6
        }
        updated_list = []

        for key, value in mash_values_not_compared.items():
            if not value:
                updated_list.append(list_value[key])

        return updated_list

    @staticmethod
    def update_cell_to_ignore(mash_data, mash_columns_not_to_compare):
        formatted_mash_row = mash_data
        for value in mash_columns_not_to_compare:
            formatted_mash_row[value] = 'no data'

        return formatted_mash_row

    @staticmethod
    def pcb_side(recipe_path: str) -> str:
        sides = ['bot', 'top']
        recipe_name = (helper.Helpers().get_filename_from_path(recipe_path)).lower()
        side_result = 'no_side'
        for side in sides:
            if side in recipe_name:
                side_result = side

        return side_result

    @staticmethod
    def get_board_side_data(mash_data, side) -> dict:
        board_side_data = {}
        mash = mash_data[2]
        if side != 'no_side':
            for part, value in mash.items():
                if isinstance(value[1], float) is False and side in value[6].lower() and not isinstance(value[8], float) and value[8].lower() != 'tht' and value[7].lower() != 'no' and value[7].lower() != 'nm':
                    board_side_data[part] = {'component': value[0], 'part': value[1], 'Type': value[8],
                                             'mount': value[7]}
        else:
            for part, value in mash.items():
                if not isinstance(value[1], float) is False and value[8].lower() != 'tht' and value[7].lower() != 'no' and value[7].lower() != 'nm':
                    board_side_data[part] = {'component': value[0], 'part': value[1], 'Type': value[8],
                                             'mount': value[7]}

        return board_side_data

    @staticmethod
    def parse_recipe_folder_path(path_to_recipe):
        recipe_file_name = helper.Helpers().get_filename_from_path(path_to_recipe)
        recipe_folder_path = path_to_recipe.replace('/' + recipe_file_name, '')

        return recipe_folder_path

    @staticmethod
    def compare_recipe_to_mash(recipe_path: str, mash_data) -> list:
        table = []
        mash_components = mash_data
        file = recipe_path + '/tmp/0.board'
        with open(file, 'rb') as f:
            gzip_stream = io.BytesIO(f.read())
            with gzip.GzipFile(fileobj=gzip_stream, mode='rb') as f:
                gzip_stream = io.BytesIO(f.read())
                data = xmltodict.parse(gzip_stream)
                elements = data['Board']['Children']['a:Element']
                for element in elements:
                    component_name = str(element['a:Name'])
                    part_name = str(element['PartNumber'])
                    if component_name in mash_components:
                        if mash_components[component_name]['part'].lower() not in part_name.lower():
                            table.append([component_name, part_name, mash_components[component_name]['part'],
                                          mash_components[component_name]['mount'],
                                          mash_components[component_name]['Type']])
                        del mash_components[component_name]
                    elif component_name not in mash_components and 'PART' not in part_name and 'Template_FOD' not in part_name:
                        table.append([component_name, part_name, 'empty', 'empty', 'empty'])
                if mash_components:
                    for component, value in mash_components.items():
                        table.append([component, 'empty', value['part'], value['mount'], value['Type']])
                if not table:
                    table.append(['All components validated!!', 'All components validated!!', 'All components validated!!'])
        shutil.rmtree(recipe_path + '/tmp/')
        return table
