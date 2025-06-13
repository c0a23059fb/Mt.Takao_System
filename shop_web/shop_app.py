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
        host='db',
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
    """
    QRコード画像を受け取り、デコードして結果を返す
    - 初回読み込み時はDBのcoupon_validをFALSEに更新（使用済みにする）
    - 2回目以降は「使用済み」と判定
    """
    try:
        # 画像データを受け取りデコード
        data = request.json['image']
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        decoded_objects = pyzbar.decode(gray)
        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')  # QRコードの内容（文字列）
            # DBでクーポン状態を確認・更新
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT coupon_valid FROM Users WHERE coupon_code=%s"
                cursor.execute(sql, (qr_data,))
                row = cursor.fetchone()
                if row is None:
                    conn.close()
                    return jsonify({"success": False, "error": "無効なクーポンです", "redirect": "/failure"})
                elif not row['coupon_valid']:  # coupon_valid が False (=0)なら使用済み
                    conn.close()
                    print("使用済みクーポン:", qr_data)
                    return jsonify({"success": False, "error": "使用済みクーポンです", "redirect": "/used"})
                else:
                    # 初回利用なので使用済みに更新
                    update_sql = "UPDATE Users SET coupon_valid=FALSE WHERE coupon_code=%s"
                    cursor.execute(update_sql, (qr_data,))
                    conn.commit()
            conn.close()
            # QRコードの内容（文字列）はqr_dataで取得できる。必要ならログや別テーブルに保存可能
            print("QRコードデータ:", qr_data)
            return jsonify({"success": True, "data": qr_data, "redirect": "/success"})
        else:
            # QRコードが検出できなかった場合
            print("No QR code detected")
            return jsonify({"success": False, "error": "QRコードが検出できませんでした", "redirect": "/failure"})
    except Exception as e:
        # 例外発生時
        print("Exception during scan:", str(e))
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