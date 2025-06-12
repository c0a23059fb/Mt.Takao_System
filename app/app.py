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
import re
from datetime import datetime

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
        data = request.get_json()
        if 'image' not in data:
            return "No image provided", 400
        # Base64のヘッダーを除去して画像を保存
        img_data = re.sub('^data:image/.+;base64,', '', data['image'])
        img_binary = base64.b64decode(img_data)

        os.makedirs('memorys', exist_ok=True)
        filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
        filepath = f'memorys/{filename}'
        with open(filepath, 'wb') as f:
            f.write(img_binary)

        return f"保存成功: {filename}"

    except Exception as e:
        print(f"Error: {e}")  # デバッグ用ログ
        return jsonify({"success": False, "error": str(e)})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 現在のファイルのディレクトリを取得

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    ログイン画面を表示し、ユーザー情報をデータベースに保存するエンドポイント。
    - GET（通常）：ログイン画面を表示
    - GET（QRコード経由）：クエリでログイン試行
    - POST（フォーム送信）：ログイン試行

    Returns:
        login_succes.html（成功時）、
        login.html（エラー時またはGET時）
    """
    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
    else:
        # クエリパラメータから取得（QRコードからの自動ログイン用）
        user_name = request.args.get('user_name')
        password = request.args.get('password')

        # クエリが無い通常GETアクセスなら、ログイン画面を表示
        if not user_name or not password:
            return render_template('login.html')

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
    data = request.get_json()
    if 'image' not in data:
        return "No image provided", 400
    try:

        # Base64のヘッダーを除去して画像を保存
        img_data = re.sub('^data:image/.+;base64,', '', data['image'])
        img_binary = base64.b64decode(img_data)

        os.makedirs('memorys', exist_ok=True)
        filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
        filepath = f'memorys/{filename}'
        with open(filepath, 'wb') as f:
            f.write(img_binary)

        return f"保存成功: {filename}"
    except Exception as e:
        print(f"エラー: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/checkpoint')
@login_required
def viw_points():
    return render_template("checkpoint.html")

if __name__ == '__main__':
    """
    アプリケーションのエントリーポイント。
    FlaskアプリケーションをSSLを使用して起動します。
    """
    app.run(host='0.0.0.0', port=8000, ssl_context=context)
