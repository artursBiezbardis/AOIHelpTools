import sqlite3 as sql


class SQLiteRepository:

    def connectToDB(self, location):

        return (sql.connect(location))

    def checkIfEnteryExist(self, table, selectedCol, entry, location):
        conn = self.connectToDB(location)
        c = conn.cursor()
        query = "SELECT * FROM "+table+" WHERE "+selectedCol+"=?"
        c.execute(query, (entry,))
        results = c.fetchall()
        conn.close()
        if results:
            return True
        else:
            return False

    def read_value_by_name(self, table, name, location):
        conn = self.connectToDB(location)
        c = conn.cursor()
        query = "SELECT * FROM " + table + " WHERE Name =?"
        c.execute(query, (name,))
        value = c.fetchone()
        conn.close()
        return value[1]

    def set_value_by_name(self, table, name, location, value):
        conn = self.connectToDB(location)
        c = conn.cursor()
        c.execute("UPDATE "+table+" SET Value = ? WHERE Name = ?", (value, name))
        test = self.read_value_by_name(table, name, location)
        conn.commit()
