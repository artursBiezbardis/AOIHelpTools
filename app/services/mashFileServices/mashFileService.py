import app.repositories.mashFileRepository.mashFileRepository as mashFileRepo
import re
import helpers.helpers as helper
import numpy as np
import json


class MashFileService:

    def extract_mash_data(self, location):

        mash_table = mashFileRepo.MashFileRepository().get_mash_table(location)
        component_names = []
        mash_data = {}
        file_name = helper.Helpers().get_filename_from_path(location)
        for item in mash_table:
            if not isinstance(item[0], (int, float, complex)):
                component_name = item[0].strip()
                if self.is_valid_component_name(component_name):
                    item = np.array(item)
                    item = item.tolist()
                    item = self.format_data_content(item)
                    mash_data[component_name] = item
                    component_names.append(component_name)
        results = [file_name, component_names, mash_data]

        return results

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
        component = item
        for key, value in enumerate(component):
            if key >= 10:
                del component[key]
            else:
                if not isinstance(value, (int, float)):
                    str_value = str(value).strip().replace(",", ".")

                    if not helper.Helpers().is_number(str_value):
                        str_value = str_value.upper()
                        str_value = helper.Helpers().replace_special_letters(str_value)
                    else:
                        str_value = float(str_value)

                    component[key] = str_value

        return component

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
