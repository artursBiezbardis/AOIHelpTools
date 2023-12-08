import app.services.groupComponentsByLocationService.goupComponentsByLocationService as prepareRecipe
import app.services.mashFileServices.mashFileService as mashService
import re
import helpers.helpers as helper
import os
import json


class CompareRecipeMashService:

    def main(self, recipe_path, mash_path):

        prepare_recipe = prepareRecipe.GroupComponentsByLocation()

        mash_service = mashService.MashFileService()
        board_side = self.pcb_side(recipe_path)
        mash_data = mash_service.extract_mash_data(mash_path)
        board_side_mash_data = self.get_board_side_data(mash_data, board_side)
        prepare_recipe.prepare_recipe_data(self.parse_recipe_folder_path(recipe_path))

        table = []

        return table

    def compare_two_mashes(self, location1, location2, mash_values_not_compared):

        empty_row = ['', '', '', '', '', '', '', '', '', '']
        compare_table = []
        mash1 = self.extract_mash_data(location1)
        mash2 = self.extract_mash_data(location2)
        file_name1 = mash1[0]
        file_name2 = mash2[0]
        comp_name_list1 = mash1[1]
        comp_name_list2 = mash2[1]
        mash_data1 = mash1[2]
        mash_data2 = mash2[2]
        comp_list = self.get_list_of_components_from_mashes(comp_name_list1, comp_name_list2)
        row_count = 0
        cells_with_differences = []
        mash_columns_not_to_compare = self.convert_to_list_mash_columns_not_to_compare(mash_values_not_compared)

        for component in comp_list:
            no_data = ['no data', 'no data', 'no data', 'no data', 'no data', 'no data', 'no data', 'no data',
                       'no data', 'no data']
            if component not in mash_data1:
                mash_data1[component] = no_data
            if component not in mash_data2:
                mash_data2[component] = no_data

            mash_data1[component] = self.update_cell_to_ignore(mash_data1[component],
                                                               mash_columns_not_to_compare)
            mash_data2[component] = self.update_cell_to_ignore(mash_data2[component],
                                                               mash_columns_not_to_compare)
            if json.dumps(mash_data1[component]) != json.dumps(mash_data2[component]):
                row_count += 1
                data_row1 = mash_data1[component]
                data_row2 = mash_data2[component]

                # adds differences location in 3D array first value in 2D array is row number for adding colors to excel export
                data_row_diff_location = self.locate_diff_in_row(row_count, data_row1, data_row2)
                cells_with_differences.append(data_row_diff_location[0])
                cells_with_differences.append(data_row_diff_location[1])
                data_row1.insert(0, file_name1)
                data_row2.insert(0, file_name2)
                compare_table.append(data_row1)
                compare_table.append(data_row2)
                compare_table.append(empty_row)
                row_count += 2

        return [compare_table, cells_with_differences]

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
                if side in value[6].lower() and isinstance(value[1], float) is False and value[8].lower() != 'tht' and \
                        value[8].lower() != 'hmt' and value[7].lower() != 'no':
                    board_side_data[part] = {'component': value[0], 'part': value[1], 'Type': value[8],
                                             'mount': value[7]}
        else:
            for part, value in mash.items():
                if isinstance(value[1], float) is False and value[8].lower() != 'tht' and \
                        value[8].lower() != 'hmt' and value[7].lower() != 'no':
                    board_side_data[part] = {'component': value[0], 'part': value[1], 'Type': value[8],
                                             'mount': value[7]}

        return board_side_data

    @staticmethod
    def parse_recipe_folder_path(path_to_recipe):
        recipe_file_name = helper.Helpers().get_filename_from_path(path_to_recipe)
        recipe_folder_path = path_to_recipe.replace('/' + recipe_file_name, '')

        return recipe_folder_path
