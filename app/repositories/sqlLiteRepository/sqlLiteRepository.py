import sqlite3 as sql


class SQLiteRepository:

    @staticmethod
    def connect_to_db(location):

        return sql.connect(location)

    def check_if_entry_exist(self, table, selected_col, entry,
                             location):
        conn = self.connect_to_db(location)
        c = conn.cursor()
        query = "SELECT * FROM " + table + " WHERE " + selected_col + "=?"
        c.execute(query, (entry,))
        results = c.fetchall()
        conn.close()
        if results:

            return True
        else:

            return False

    def read_value_by_name(self, table, name,
                           data_base):
        conn = self.connect_to_db(data_base)
        c = conn.cursor()
        query = "SELECT * FROM " + table + " WHERE Name =?"
        c.execute(query, (name,))
        value = c.fetchone()
        conn.close()

        return value[1]

    def set_value_by_name(self, table, name, value,
                          data_base):
        conn = self.connect_to_db(data_base)
        c = conn.cursor()
        c.execute("UPDATE " + table + " SET Value = ? WHERE Name = ?", (value, name))
        conn.commit()
        conn.close()

    def get_all(self, table, data_base):

        conn = self.connect_to_db(data_base)
        c = conn.cursor()
        query = "SELECT * FROM " + table + ""
        c.execute(query)
        settings_list = c.fetchall()
        conn.close()

        return settings_list

    def get_component_package_name(self, table, name, data_base):

        conn = self.connect_to_db(data_base)
        c = conn.cursor()
        query = f'SELECT packageName FROM {table} WHERE TemplateId = ?'
        c.execute(query, (name,))
        package_names = c.fetchone()
        conn.close()

        return package_names
