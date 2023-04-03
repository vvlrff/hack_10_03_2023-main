import sqlite3


class DB:

    def __init__(self):
        self.conn = sqlite3.connect('uav_data.db')
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS uav_data(
           "id" INTEGER PRIMARY KEY,
           "tag" CHAR(255),
           "brand" CHAR(255),
           "name" CHAR(255),
           "price" CHAR(255),
           "specifications" CHAR(255));
        """)
        self.conn.commit()

    def db_cleaning(self):
        try:
            self.cur.execute("""DELETE FROM uav_data;""")
            self.conn.commit()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def insert_into_db(self, new_line):
        self.cur.execute("INSERT INTO uav_data VALUES(NULL, ?, ?, ?, ?, ?);", new_line)
        self.conn.commit()

    def read_db(self):
        sqlite_connection = None
        result = []

        try:
            sqlite_connection = sqlite3.connect('uav_data.db')
            cursor = sqlite_connection.cursor()

            cursor.execute("SELECT * from uav_data")
            records = cursor.fetchall()

            for row in records:
                result.append(
                    {"tag": row[1], "brand": row[2], "name": row[3], "price": row[4], "specifications": row[5]})

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return result
