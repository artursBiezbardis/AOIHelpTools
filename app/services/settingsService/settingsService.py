import app.repositories.sqlLiteRepository.sqlLiteRepository as sqlLite


class Settings:
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

    def settings_collection(self, settings_view_values):
        return
