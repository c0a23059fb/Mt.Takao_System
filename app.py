from flask import Flask, request, jsonify, render_template
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
import ssl
from dotenv import load_dotenv
import sqlite3

# Flaskアプリケーションの初期化
app = Flask(
    __name__,
    static_folder='Front/static',  # 静的ファイルのディレクトリ
    template_folder='Front/templates'  # HTMLテンプレートのディレクトリ
)

# SSL証明書のパスを設定
load_dotenv()
cert_path = os.path.join(os.path.dirname(__file__), 'keys', 'new_cert.pem')  # SSL証明書の絶対パス
key_path = os.path.join(os.path.dirname(__file__), 'keys', 'new_key.pem')   # SSL秘密鍵の絶対パス

# SSLコンテキストの設定
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)

@app.route('/')
def home():
    """
    ホーム画面を表示するエンドポイント。
    Returns:
        HTMLテンプレート: Home.html
    """
    return render_template('Home.html')

@app.route('/qr_road')
def qr_road():
    """
    QRコード読み取り画面を表示するエンドポイント。
    Returns:
        HTMLテンプレート: qr_road.html
    """
    return render_template('qr_road.html')

@app.route('/shop')
def shop():
    """
    周辺検索画面を表示するエンドポイント。
    Returns:
        HTMLテンプレート: shop.html
    """
    return render_template('shop.html')

@app.route('/scan', methods=['POST'])
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
    if request.method == 'POST':
        email = request.form.get('email')
        userid = request.form.get('userid')
        password = request.form.get('password')

        # デバッグログで値を確認
        print(f"[ログイン] Email: {email}, ID: {userid}, Password: {password}")

        # データベースに保存
        try:
            conn = sqlite3.connect('user_data.db')  # SQLiteデータベースに接続
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    userid TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')  # テーブルが存在しない場合は作成
            cursor.execute('INSERT INTO users (email, userid, password) VALUES (?, ?, ?)', (email, userid, password))
            conn.commit()
            conn.close()
            print("データベースに保存しました")
        except Exception as e:
            print(f"データベースエラー: {e}")

        # ユーザー名を表示した後、home画面に遷移
        return render_template('login_succes.html', userid=userid)

    return render_template('login.html')

if __name__ == '__main__':
    """
    アプリケーションのエントリーポイント。
    FlaskアプリケーションをSSLを使用して起動します。
    """
    app.run(host='0.0.0.0', port=8000, ssl_context=context)
