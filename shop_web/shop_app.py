from flask import Flask, request, render_template, jsonify
import pymysql
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
import pymysql  # MySQL接続用

# Flaskアプリケーションの初期化
app = Flask(
    __name__,
    static_folder='static',      # 静的ファイル（JSやCSS）のディレクトリ
    template_folder='template'   # HTMLテンプレートのディレクトリ
)

# データベース接続関数
def get_db_connection():
    # 必要に応じてhost, user, password, databaseを変更
    return pymysql.connect(
        host='localhost',
        user='root',
        password='passwordA1!',
        database='main_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# トップページ（QRコード読み取り画面）
@app.route('/')
def index():
    """
    QRコード読み取り画面を表示
    """
    return render_template('qr_reader.html')

# QRコード画像を受け取り、デコード・DB判定・状態更新
@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.get_json()
        qr_data = data.get('code')  # 文字列で受け取る

        if not qr_data:
            return jsonify({"success": False, "error": "QRコードデータがありません", "redirect": "/failure"})

        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT coupon_valid FROM Users WHERE coupon_code=%s"
            cursor.execute(sql, (qr_data,))
            row = cursor.fetchone()
            if row is None:
                conn.close()
                return jsonify({"success": False, "error": "無効なクーポンです", "redirect": "/failure"})
            elif not row['coupon_valid']:
                conn.close()
                return jsonify({"success": False, "error": "使用済みクーポンです", "redirect": "/used"})
            else:
                update_sql = "UPDATE Users SET coupon_valid=FALSE WHERE coupon_code=%s"
                cursor.execute(update_sql, (qr_data,))
                conn.commit()
        conn.close()
        return jsonify({"success": True, "data": qr_data, "redirect": "/success"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "redirect": "/failure"})

# QRコード読み取り成功画面
@app.route('/success')
def success():
    """
    QRコード読み取り成功画面
    """
    return render_template('success.html')

# QRコード読み取り失敗画面
@app.route('/failure')
def failure():
    """
    QRコード読み取り失敗画面
    """
    return render_template('failure.html')

# クーポン使用済み画面
@app.route('/used')
def used():
    """
    QRコードが使用済みだった場合の画面
    """
    return render_template('used.html')

# アプリケーションのエントリーポイント
if __name__ == '__main__':
    # デバッグモードで0.0.0.0:8080で起動
    app.run(host='0.0.0.0', port=8080, debug=True)