import sqlite3 as sql
import root


class SQLiteRepository:

    def connectToDB(self, location):

        return (sql.connect(location))

    def checkIfEnteryExist(self, table, selectedCol, entry,
                           location):
        conn = self.connectToDB(location)
        c = conn.cursor()
        query = "SELECT * FROM " + table + " WHERE " + selectedCol + "=?"
        c.execute(query, (entry,))
        results = c.fetchall()
        conn.close()
        if results:
            return True
        else:
            return False

    def read_value_by_name(self, table, name,
                           data_base):
        conn = self.connectToDB(data_base)
        c = conn.cursor()
        query = "SELECT * FROM " + table + " WHERE Name =?"
        c.execute(query, (name,))
        value = c.fetchone()
        conn.close()
        return value[1]

    def set_value_by_name(self, table, name, value,
                          data_base):
        conn = self.connectToDB(data_base)
        c = conn.cursor()
        c.execute("UPDATE " + table + " SET Value = ? WHERE Name = ?", (value, name))
        conn.commit()
        conn.close()

    def get_all(self, table, data_base):
        conn = self.connectToDB(data_base)
        c = conn.cursor()
        query = "SELECT * FROM " + table + ""
        c.execute(query)
        settings_list = c.fetchall()
        conn.close()
        return settings_list
