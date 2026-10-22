import json
import math
import re

import app.repositories.mashFileRepository.mashFileRepository as mashFileRepo
import helpers.helpers as helper


class MashFileService:
    _COMPONENT_NAME_RE = re.compile(r'[a-zA-Z]+\d{1,7}\Z')
    _HELPER = helper.Helpers()
    _MASH_FIELD_COUNT = 10
    _NO_DATA = 'no data'

    def extract_mash_data(self, location):

        mash_table = mashFileRepo.MashFileRepository().get_mash_table(location)
        component_names = []
        mash_data = {}
        file_name = self._HELPER.get_filename_from_path(location)
        is_component_name = self._COMPONENT_NAME_RE.fullmatch
        for item in mash_table:
            name_cell = item[0]
            if isinstance(name_cell, (int, float, complex)):
                continue
            component_name = name_cell.strip()
            if is_component_name(component_name) is None:
                continue
            row = item.tolist() if hasattr(item, 'tolist') else list(item)
            mash_data[component_name] = self.format_data_content(row)
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
            if component not in mash_data1:
                mash_data1[component] = [self._NO_DATA] * self._MASH_FIELD_COUNT
            if component not in mash_data2:
                mash_data2[component] = [self._NO_DATA] * self._MASH_FIELD_COUNT

            row1 = self.update_cell_to_ignore(mash_data1[component], mash_columns_not_to_compare)
            row2 = self.update_cell_to_ignore(mash_data2[component], mash_columns_not_to_compare)
            if self._rows_differ(row1, row2):
                row_count += 1

                # adds differences location in 3D array first value in 2D array is row number for adding colors to excel export
                data_row_diff_location = self.locate_diff_in_row(row_count, row1, row2)
                cells_with_differences.append(data_row_diff_location[0])
                cells_with_differences.append(data_row_diff_location[1])
                row1.insert(0, file_name1)
                row2.insert(0, file_name2)
                compare_table.append(row1)
                compare_table.append(row2)
                compare_table.append(empty_row)
                row_count += 2

        return [compare_table, cells_with_differences]

    @staticmethod
    def _rows_differ(left, right):
        """Match json.dumps list comparison without serializing equal rows."""
        if len(left) != len(right):
            return True
        for item1, item2 in zip(left, right):
            if item1 == item2 and type(item1) is type(item2):
                if isinstance(item1, float) and math.copysign(1.0, item1) != math.copysign(1.0, item2):
                    return True
                continue
            if (
                isinstance(item1, float)
                and isinstance(item2, float)
                and type(item1) is type(item2)
                and math.isnan(item1)
                and math.isnan(item2)
            ):
                continue
            if json.dumps(item1) != json.dumps(item2):
                return True
        return False

    @staticmethod
    def get_list_of_components_from_mashes(comp_name_list1, comp_name_list2):
        return sorted(set(comp_name_list1).union(comp_name_list2))

    @classmethod
    def is_valid_component_name(cls, name):
        try:
            return cls._COMPONENT_NAME_RE.fullmatch(name) is not None
        except TypeError:
            return False

    @staticmethod
    def locate_diff_in_row(row, mash_data1, mash_data2):
        diff1 = [row]
        diff1.extend(
            index for index, (item1, item2) in enumerate(zip(mash_data1, mash_data2)) if item1 != item2
        )
        diff2 = diff1.copy()
        diff2[0] = row + 1
        return [diff1, diff2]

    @classmethod
    def format_data_content(cls, item):
        # Compare and export use the first 10 mash fields. Dropping the tail by
        # index while iterating skipped columns and raised once a row was wide enough.
        component = item[:cls._MASH_FIELD_COUNT]
        text = cls._HELPER
        for key, value in enumerate(component):
            if isinstance(value, (int, float)):
                continue
            str_value = str(value).strip().replace(",", ".")
            if text.is_number(str_value):
                component[key] = float(str_value)
            else:
                component[key] = text.replace_special_letters(str_value.upper())
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
