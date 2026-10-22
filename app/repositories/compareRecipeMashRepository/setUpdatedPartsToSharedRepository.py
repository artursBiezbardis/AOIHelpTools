import utilities.gzipStreamUtilities as gzipStream
import utilities.fileAndFolderPathUtilities as pathUtilities
import app.repositories.sqlLiteRepository.sqlLiteRepository as sqlRepo

class SetUpdatedPartsToSharedRepository:

    dBSubLocation = '/TemplateLibrary/Templates.db'
    table = 'Component'

    def main(self, parts_list, panel_path):
        data = gzipStream.GzipStreamUtilities().parse_gzip_stream(panel_path)
        package_list = self.get_parts_pakages(parts_list, panel_path)
        updated_data = self.update_panel_parts(data, parts_list, package_list)
        gzipStream.GzipStreamUtilities().update_gzip_stream(updated_data, panel_path)
    @staticmethod
    def update_panel_parts(data, part_list, package_list):
        panel_data = data

        for element in panel_data['Panel']['PartLibrary']['a:RootTemplates']['a:_templatePropertyDecorators']['b:KeyValueOfstringTemplatePropertyDecoratorDVHnpzMe']:
            try:
                if element['b:Key'] in part_list:
                    element['b:Value']['c:TemplateLocation'] = 'Shared'
            except TypeError as e:
                print(e)
        for element in data['Panel']['PackageLibrary']['a:RootTemplates']['a:_templatePropertyDecorators']['b:KeyValueOfstringTemplatePropertyDecoratorDVHnpzMe']:
            try:
                if element['b:Key'] in package_list:
                    element['b:Value']['c:TemplateLocation'] = 'Shared'
            except TypeError as e:
                print(e)

        return panel_data

    def get_parts_pakages(self, parts_list, panel_path):

        package_list = []
        recipe_folder = pathUtilities.FileAndFolderPathUtilities().get_folder_path_from_file_path(panel_path)
        local_library_path = recipe_folder + self.dBSubLocation
        for part in parts_list:
            package = sqlRepo.SQLiteRepository().get_component_package_name(self.table, part, local_library_path)
            if package is not None:
                package_list.append(package[0])

        package_list = self.remove_list_duplicates(package_list)
        package_list = self.filter_list_remove_values(package_list)

        return package_list

    @staticmethod
    def remove_list_duplicates(duplicates_list):
        edit_list = duplicates_list
        no_duplicates_list = list(set(edit_list))
        return no_duplicates_list

    @staticmethod
    def filter_list_remove_values(list_to_filter: list, values_to_remove: list=[None]) -> list:
        common_values = set(list_to_filter) & set(values_to_remove)
        filtered_list = list_to_filter
        if common_values:
            for val in common_values:
                while val in filtered_list:
                    filtered_list.remove(val)

        return filtered_list
