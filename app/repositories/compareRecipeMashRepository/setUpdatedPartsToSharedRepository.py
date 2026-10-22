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
        if not parts_list:
            return []
        recipe_folder = pathUtilities.FileAndFolderPathUtilities().get_folder_path_from_file_path(panel_path)
        local_library_path = recipe_folder + self.dBSubLocation
        placeholders = ','.join('?' for _ in parts_list)
        query = f'SELECT packageName FROM {self.table} WHERE TemplateId IN ({placeholders})'
        with sqlRepo.SQLiteRepository.connect_to_db(local_library_path) as conn:
            rows = conn.execute(query, tuple(parts_list)).fetchall()
        return list({row[0] for row in rows if row[0] is not None})

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
