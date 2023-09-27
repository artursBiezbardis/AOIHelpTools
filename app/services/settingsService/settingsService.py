import app.repositories.sqlLiteRepository.sqlLiteRepository as sqlLite


class SettingsService:
    def read_settings_values(self, settings):
        return

    def update_settings_value(self, settings):
        sqlLite.SQLiteRepository().set_value_by_name(
            self.settings_table,
            name,
            self.data_base,
            values[name]
        )
        input_value = sqlLite.SQLiteRepository().read_value_by_name(
            self.settings_table,
            name,
            self.data_base
        )
        return input_value

    def settings_list_to_object(self, all_settings):
        all_settings_obj = {}
        for name, val in all_settings:
            all_settings_obj[name] = val

        return all_settings_obj
