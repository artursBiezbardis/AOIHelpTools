import sqlite3 as sql


class SQLiteRepository:

    @staticmethod
    def connect_to_db(location):

        return sql.connect(location)

    def check_if_entry_exist(self, table, selected_col, entry,
                             location):
        query = f'SELECT 1 FROM {table} WHERE {selected_col}=? LIMIT 1'
        with self.connect_to_db(location) as conn:
            row = conn.execute(query, (entry,)).fetchone()
        return row is not None

    def read_value_by_name(self, table, name,
                           data_base):
        query = f'SELECT Value FROM {table} WHERE Name =?'
        with self.connect_to_db(data_base) as conn:
            value = conn.execute(query, (name,)).fetchone()

        return value[0]

    def set_value_by_name(self, table, name, value,
                          data_base):
        with self.connect_to_db(data_base) as conn:
            conn.execute(
                f'UPDATE {table} SET Value = ? WHERE Name = ?',
                (value, name),
            )

    def get_all(self, table, data_base):
        with self.connect_to_db(data_base) as conn:
            return conn.execute(f'SELECT * FROM {table}').fetchall()

    def get_component_package_name(self, table, name, data_base):
        query = f'SELECT packageName FROM {table} WHERE TemplateId = ? LIMIT 1'
        with self.connect_to_db(data_base) as conn:
            return conn.execute(query, (name,)).fetchone()

    def lookup_component_package(self, table, column, entry, data_base):
        """Return (found, package_name) for one recipe database.

        Component searches read packageName with the same TemplateId predicate,
        so one query replaces the old existence scan plus a second lookup.
        Package searches still resolve packageName by TemplateId. A missing
        package row raises TypeError, matching the previous fetchone()[0].
        """
        package_query = f'SELECT packageName FROM {table} WHERE TemplateId = ? LIMIT 1'
        with self.connect_to_db(data_base) as conn:
            if column == 'TemplateId':
                row = conn.execute(package_query, (entry,)).fetchone()
                if row is None:
                    return False, None
                return True, row[0]

            found = conn.execute(
                f'SELECT 1 FROM {table} WHERE {column} = ? LIMIT 1',
                (entry,),
            ).fetchone()
            if found is None:
                return False, None
            row = conn.execute(package_query, (entry,)).fetchone()
            return True, row[0]
