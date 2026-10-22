import sqlite3 as sql


class SQLiteRepository:

    @staticmethod
    def connect_to_db(location):

        return sql.connect(location)

    def check_if_entry_exist(self, table, selected_col, entry,
                             location):
        conn = self.connect_to_db(location)
        try:
            c = conn.cursor()
            query = "SELECT 1 FROM " + table + " WHERE " + selected_col + "=? LIMIT 1"
            c.execute(query, (entry,))
            return c.fetchone() is not None
        finally:
            conn.close()

    def lookup_recipe_component(self, table, selected_col, entry, location):
        """Existence check and package lookup share one connection.

        The package query stays keyed by TemplateId, matching get_component_package_name.
        """
        conn = self.connect_to_db(location)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM " + table + " WHERE " + selected_col + "=? LIMIT 1",
                (entry,),
            )
            if cursor.fetchone() is None:
                return False, None
            cursor.execute(
                "SELECT packageName FROM " + table + " WHERE TemplateId = ?",
                (entry,),
            )
            return True, cursor.fetchone()
        finally:
            conn.close()

    def get_component_package_names(self, table, names, data_base):
        if not names:
            return []
        conn = self.connect_to_db(data_base)
        try:
            cursor = conn.cursor()
            query = "SELECT packageName FROM " + table + " WHERE TemplateId = ?"
            packages = []
            for name in names:
                cursor.execute(query, (name,))
                package = cursor.fetchone()
                if package is not None:
                    packages.append(package[0])
            return packages
        finally:
            conn.close()

    def set_values_by_name(self, table, updates, data_base):
        if not updates:
            return
        conn = self.connect_to_db(data_base)
        try:
            cursor = conn.cursor()
            cursor.executemany(
                "UPDATE " + table + " SET Value = ? WHERE Name = ?",
                updates,
            )
            conn.commit()
        finally:
            conn.close()

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
