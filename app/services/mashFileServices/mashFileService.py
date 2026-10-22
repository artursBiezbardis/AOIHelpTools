import app.repositories.mashFileRepository.mashFileRepository as mashFileRepo
import re
import helpers.helpers as helper
import math


_helpers = helper.Helpers()
_COMPONENT_NAME_RE = re.compile(r'[a-zA-Z]+\d{1,7}')


class MashFileService:

    def extract_mash_data(self, location):

        mash_table = mashFileRepo.MashFileRepository().get_mash_table(location)
        component_names = []
        mash_data = {}
        file_name = _helpers.get_filename_from_path(location)
        valid_name = self.is_valid_component_name
        format_row = self.format_data_content
        for item in mash_table:
            raw_name = item[0]
            if isinstance(raw_name, (int, float, complex)):
                continue
            component_name = raw_name.strip()
            if valid_name(component_name):
                to_list = getattr(item, 'tolist', None)
                row_values = to_list() if to_list is not None else list(item)
                mash_data[component_name] = format_row(row_values)
                component_names.append(component_name)
        return [file_name, component_names, mash_data]

    def compare_two_mashes(self, location1, location2, mash_values_not_compared):

        empty_row = ['', '', '', '', '', '', '', '', '', '']
        compare_table = []
        mash1 = self.extract_mash_data(location1)
        mash2 = self.extract_mash_data(location2)
        file_name1 = mash1[0]
        file_name2 = mash2[0]
        mash_data1 = mash1[2]
        mash_data2 = mash2[2]
        comp_list = self.get_list_of_components_from_mashes(mash1[1], mash2[1])
        row_count = 0
        cells_with_differences = []
        mash_columns_not_to_compare = self.convert_to_list_mash_columns_not_to_compare(mash_values_not_compared)
        rows_differ = self.rows_differ
        update_cell_to_ignore = self.update_cell_to_ignore
        locate_diff_in_row = self.locate_diff_in_row

        for component in comp_list:
            no_data = ['no data', 'no data', 'no data', 'no data', 'no data', 'no data', 'no data', 'no data',
                       'no data', 'no data']
            if component not in mash_data1:
                mash_data1[component] = no_data
            if component not in mash_data2:
                mash_data2[component] = no_data

            row1 = update_cell_to_ignore(mash_data1[component], mash_columns_not_to_compare)
            row2 = update_cell_to_ignore(mash_data2[component], mash_columns_not_to_compare)
            if rows_differ(row1, row2):
                row_count += 1
                # First value in each diff record is the table row, used when coloring an export.
                data_row_diff_location = locate_diff_in_row(row_count, row1, row2)
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
    def get_list_of_components_from_mashes(comp_name_list1, comp_name_list2):
        return sorted(set(comp_name_list1).union(comp_name_list2))

    @staticmethod
    def is_valid_component_name(name):
        if not isinstance(name, str):
            return False
        return _COMPONENT_NAME_RE.fullmatch(name) is not None

    @staticmethod
    def locate_diff_in_row(row, mash_data1, mash_data2):
        diff1 = [row]
        for index, (item1, item2) in enumerate(zip(mash_data1, mash_data2)):
            if item1 != item2:
                diff1.append(index)

        diff2 = list(diff1)
        diff2[0] = row + 1

        return [diff1, diff2]

    @staticmethod
    def rows_differ(row1, row2) -> bool:
        """Same distinctions as comparing json.dumps of the two rows.

        NaN matches NaN, and 1 does not match 1.0. Signed zero stays distinct.
        """
        if len(row1) != len(row2):
            return True
        for left, right in zip(row1, row2):
            if isinstance(left, float) and isinstance(right, float):
                if math.isnan(left) and math.isnan(right):
                    continue
                if left == right and math.copysign(1.0, left) == math.copysign(1.0, right):
                    continue
                return True
            if left == right and type(left) is type(right):
                continue
            return True
        return False

    @staticmethod
    def format_data_content(item):
        component = list(item[:10])
        try_float = _helpers.try_float
        replace_special_letters = _helpers.replace_special_letters
        for key, value in enumerate(component):
            if isinstance(value, (int, float)):
                continue
            text = str(value).strip().replace(',', '.')
            parsed = try_float(text)
            if parsed is None:
                component[key] = replace_special_letters(text.upper())
            else:
                component[key] = parsed

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
