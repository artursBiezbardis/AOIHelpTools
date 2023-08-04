import numpy

import app.repositories.mashFileRepository.mashFileRepository as mashFileRepo
import re
import helpers.helpers as help
import numpy as np


class MashFileService:
    testLocation = 'Z:\cad\I0MTPI43_R02\I0MTPI43_R02_mash_01.xls'

    def extract_mash_data(self, location):

        mash_table = mashFileRepo.MashFileRepository().get_mash_table(location)
        component_names = []
        mash_data = {}
        file_name = help.Helpers().get_filename_from_path(location)
        for item in mash_table:

            if self.is_valid_component_name(item[0]):
                item = np.array(item)
                item = item.tolist()
                item.insert(0, file_name)
                mash_data[item[1]] = item
                component_names.append(item[1])
        results = [file_name, component_names, mash_data]

        return results

    def compare_two_mashes(self, location1, location2):

        mash1 = self.extract_mash_data(location1)
        mash2 = self.extract_mash_data(location2)
        file_name1 = mash1[0]
        file_name2 = mash2[0]
        comp_name_list1 = mash1[1]
        comp_name_list2 = mash2[1]
        mash_data1 = mash1[2]
        mash_data2 = mash2[2]
        comp_list = self.get_list_of_components_from_mashes(comp_name_list1, comp_name_list2)

        print(file_name1, comp_list)

    def get_list_of_components_from_mashes(self, comp_name_list1, comp_name_list2):

        comp_name_list1.extend(comp_name_list2)
        comp_name_list = list(set(comp_name_list1))
        comp_name_list.sort()
        return comp_name_list

    def is_valid_component_name(self, name):
        try:
            return re.fullmatch(r'[a-zA-Z]+\d{1,4}', name) is not None
        except TypeError:
            return False
