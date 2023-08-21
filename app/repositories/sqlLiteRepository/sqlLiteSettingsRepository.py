import sqlite3 as sql

class Settings:

    location = 'settings.db'

    def get_setting_value(self, name):

        conn = sql.connect(self.location)
        return name
