import pymysql

class DataBase():
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='passwordA1!',
            database='main_db',
            charset='utf8mb4'
        )

    def select(self, query, params = None):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.conn.close()


# conn = DataBase()  # SQLiteデータベースに接続
# # cursor = conn.cursor()
# passwd = conn.select("SELECT password FROM Users WHERE user_name = 'user094'")
# print(passwd)
# conn.close()