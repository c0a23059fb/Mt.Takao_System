from flask import Flask, request, session, redirect, url_for, jsonify, render_template
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
import ssl
from dotenv import load_dotenv
from functools import wraps

from modules.DataBase import DataBase


# Flaskアプリケーションの初期化
app = Flask(
    __name__,
    static_folder='Front/static',  # 静的ファイルのディレクトリ
    template_folder='Front/templates'  # HTMLテンプレートのディレクトリ
)
app.secret_key = app.secret_key = 'secret_key'
db = DataBase("db")

# SSL証明書のパスを設定
load_dotenv()
cert_path = os.path.join(os.path.dirname(__file__), 'keys', 'new_cert.pem')  # SSL証明書の絶対パス
key_path = os.path.join(os.path.dirname(__file__), 'keys', 'new_key.pem')   # SSL秘密鍵の絶対パス

# SSLコンテキストの設定
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))  # ログインページにリダイレクト
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    """
    ホーム画面を表示するエンドポイント。
    Returns:
        HTMLテンプレート: Home.html
    """
    return render_template('Home.html')

@app.route('/camera')
@login_required
def camera():
    """
    QRコード読み取り画面を表示するエンドポイント。
    Returns:
        HTMLテンプレート: camera.html
    """
    return render_template('camera.html')

@app.route('/shop')
@login_required
def shop():
    """
    周辺検索画面を表示するエンドポイント。
    Returns:
        HTMLテンプレート: shop.html
    """
    return render_template('shop.html')

@app.route('/scan', methods=['POST'])
@login_required
def scan_qr_code():
    """
    QRコードを読み取り、デコードするエンドポイント。
    POSTデータとしてBase64形式の画像を受け取り、QRコードをデコードします。

    Returns:
        JSONレスポンス: 成功時はQRコードのデータ、失敗時はエラーメッセージ。
    """
    try:
        data = request.json['image']
        print(f"Received data: {data[:100]}")  # デバッグ用ログ（データの先頭100文字を表示）
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)

        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        decoded_objects = pyzbar.decode(gray)

        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')
            return jsonify({"success": True, "data": qr_data})
        else:
            return jsonify({"success": False, "error": "No QR code detected"})
    except Exception as e:
        print(f"Error: {e}")  # デバッグ用ログ
        return jsonify({"success": False, "error": str(e)})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 現在のファイルのディレクトリを取得

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    ログイン画面を表示し、ユーザー情報をデータベースに保存するエンドポイント。
    POSTデータとしてメールアドレス、ユーザーID、パスワードを受け取り、SQLiteデータベースに保存します。

    Returns:
        HTMLテンプレート: login_succes.html（成功時）、login.html（GETリクエスト時）
    """
    if 'user' not in session:
        if request.method == 'POST':
            user_name = request.form.get('user_name')
            password = request.form.get('password')

            print(f"[ログイン試行] user_name: {user_name}, password: {password}")

            try:
                result = db.select_pass(user_name)

                if result and result == password:
                    session['user'] = user_name
                    print("ログイン成功")
                    return render_template('login_succes.html', userid=user_name)
                else:
                    print("ログイン失敗：認証情報が一致しません")
                    return render_template('login.html', error="ユーザー名またはパスワードが間違っています")
            except Exception as e:
                print(f"ログイン処理中のエラー: {e}")
                return render_template('login.html', error="システムエラーが発生しました　再度お試しください")

        return render_template('login.html')
    else:
        return redirect(url_for('home'))

@app.route('/coupons')
@login_required
def coupons():
    """
    所有しているクーポンを表示するエンドポイント。
    Returns:
        HTMLテンプレート: coupons.html
    """
    # 仮のクーポンデータ（データベースから取得する場合はここを変更）
    coupon_data = []  # 空のリストでクーポンがない状態を表す
    return render_template('coupons.html', coupons=coupon_data)

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    """
    クライアントから送信された写真をデータベースに保存するエンドポイント。
    """
    try:
        data = request.json['image']
        # Base64データをデコードしてバイナリデータに変換
        image_data = base64.b64decode(data.split(',')[1])

        # データベースに保存
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image BLOB NOT NULL
            )
        ''')
        cursor.execute('INSERT INTO photos (image) VALUES (?)', (image_data,))
        conn.commit()
        conn.close()

        return jsonify({"success": True})
    except Exception as e:
        print(f"エラー: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    """
    アプリケーションのエントリーポイント。
    FlaskアプリケーションをSSLを使用して起動します。
    """
    app.run(host='0.0.0.0', port=8000, ssl_context=context)
