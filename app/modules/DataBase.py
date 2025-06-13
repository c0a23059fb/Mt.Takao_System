import pymysql

class DataBase():
    def __init__(self, host_name = "localhost"):
        self.host = host_name

    def connect(self):
        db = pymysql.connect(
            host=self.host,
            user='root',
            password='passwordA1!',
            database='main_db',
            charset='utf8mb4'
        )
        return db

    def select_pass(self, user_name):
        query = "SELECT password FROM Users WHERE user_name = %s"
        db = self.connect()
        cursor = db.cursor()
        cursor.execute(query, (user_name,))
        result = cursor.fetchall()
        db.close()
        if result:
            return result[0][0]
        else:
            return

    def select_id(self, user_name):
        query = "SELECT id FROM Users WHERE user_name = %s"
        db = self.connect()
        cursor = db.cursor()
        cursor.execute(query, (user_name,))
        result = cursor.fetchall()
        db.close()
        if result:
            return result[0][0]
        else:
            return

    def select_coupon_valid(self, user_name):
        query = "SELECT coupon_valid FROM Users WHERE user_name = %s"
        db = self.connect()
        cursor = db.cursor()
        cursor.execute(query, (user_name,))
        result = cursor.fetchall()[0]
        db.close()
        return result[0]

    def checkAgoal(self, user_name):
        id = self.select_id(user_name)
        query = "SELECT check_valid, goal_valid FROM Check_Point WHERE user_id = %s"
        db = self.connect()
        cursor = db.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchall()[0]
        db.close()
        if result == (1, 1):
            return True
        return False