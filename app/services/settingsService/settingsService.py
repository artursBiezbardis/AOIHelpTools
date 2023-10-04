import app.repositories.sqlLiteRepository.sqlLiteRepository as sqlLite
import helpers.helpers as helper
import root


class SettingsService:
    data_base = settings_database = root.RootLocation().root_dir+'\\settings.db'
    settings_table = 'setup'

    def get_settings(self):

        return sqlLite.SQLiteRepository().get_all(self.settings_table, self.data_base)

    def update_settings_values(self, view_values):
        settings = sqlLite.SQLiteRepository().get_all(self.settings_table, self.data_base)
        for name, val in settings:
            if val is not view_values[name]:
                sqlLite.SQLiteRepository().set_value_by_name(
                    self.settings_table,
                    name,
                   view_values[name],
                    self.data_base
                )

    def get_setting(self, name):

        return helper.Helpers().correct_path_string(
            sqlLite.SQLiteRepository().read_value_by_name(self.settings_table, name, self.data_base)
        )

    @staticmethod
    def settings_list_to_object(all_settings):
        all_settings_obj = {}
        for name, val in all_settings:
            all_settings_obj[name] = val

        return all_settings_obj
