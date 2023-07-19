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
        if results:
            conn.close()
            return True
        else:
            conn.close()
            return False
