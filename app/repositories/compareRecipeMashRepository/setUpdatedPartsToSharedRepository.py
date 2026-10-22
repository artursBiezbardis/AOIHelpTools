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
        part_keys = set(part_list)
        package_keys = set(package_list)

        for element in panel_data['Panel']['PartLibrary']['a:RootTemplates']['a:_templatePropertyDecorators']['b:KeyValueOfstringTemplatePropertyDecoratorDVHnpzMe']:
            try:
                if element['b:Key'] in part_keys:
                    element['b:Value']['c:TemplateLocation'] = 'Shared'
            except TypeError as e:
                print(e)
        for element in data['Panel']['PackageLibrary']['a:RootTemplates']['a:_templatePropertyDecorators']['b:KeyValueOfstringTemplatePropertyDecoratorDVHnpzMe']:
            try:
                if element['b:Key'] in package_keys:
                    element['b:Value']['c:TemplateLocation'] = 'Shared'
            except TypeError as e:
                print(e)

        return panel_data

    def get_parts_pakages(self, parts_list, panel_path):

        recipe_folder = pathUtilities.FileAndFolderPathUtilities().get_folder_path_from_file_path(panel_path)
        local_library_path = recipe_folder + self.dBSubLocation
        package_list = sqlRepo.SQLiteRepository().get_component_package_names(
            self.table, parts_list, local_library_path)
        package_list = self.remove_list_duplicates(package_list)
        package_list = self.filter_list_remove_values(package_list)

        return package_list

    @staticmethod
    def remove_list_duplicates(duplicates_list):
        return list(dict.fromkeys(duplicates_list))

    @staticmethod
    def filter_list_remove_values(list_to_filter: list, values_to_remove=None) -> list:
        if values_to_remove is None:
            values_to_remove = (None,)
        remove = set(values_to_remove)
        if not remove:
            return list_to_filter
        return [value for value in list_to_filter if value not in remove]
