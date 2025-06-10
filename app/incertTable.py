import csv
import pymysql

# 接続情報（※ あなたの環境に合わせて変更してください）
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='passwordA1!',
    database='main_db',
    charset='utf8mb4'
)

cursor = conn.cursor()

# CSVファイルの読み込み
with open('users_with_coupons.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Usersテーブルへ挿入
        insert_user = """
        INSERT INTO Users (user_name, password, coupon_code, coupon_valid)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_user, (
            row['user_name'],
            row['password'],
            row['coupon_code'],
            row['coupon_valid'].upper() == 'TRUE'
        ))

        # 最後に挿入したユーザーのIDを取得
        user_id = cursor.lastrowid

        # Check_Pointテーブルへ挿入
        insert_cp = """
        INSERT INTO Check_Point (user_id, check_valid, goal_valid)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_cp, (user_id, False, False))

# コミットとクローズ
conn.commit()
cursor.close()
conn.close()
