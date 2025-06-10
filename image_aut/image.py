import cv2
import numpy as np
import os
from flask import Flask, request, jsonify
from image_aut.utils import crop_main_object

# データベース画像ディレクトリ
DATABASE_DIR = os.path.join(os.path.dirname(__file__), 'database')

def load_database_images():
    """データベース内の画像をすべて読み込む"""
    images = []
    for fname in os.listdir(DATABASE_DIR):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = cv2.imread(os.path.join(DATABASE_DIR, fname), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
    return images

def extract_features(image):
    """画像から特徴点と記述子を抽出（主オブジェクト領域のみ）"""
    cropped = crop_main_object(image)
    orb = cv2.ORB_create(nfeatures=1000)
    keypoints, descriptors = orb.detectAndCompute(cropped, None)
    return keypoints, descriptors

def match_images(des1, des2, kp1=None, kp2=None, ratio_thresh=0.75):
    """特徴点マッチングとinlier数算出"""
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    if des1 is None or des2 is None:
        return 0, 0.0, 0
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < ratio_thresh * n.distance:
            good.append(m)
    match_count = len(good)
    match_rate = match_count / max(len(des1), len(des2))
    inliers = 0
    if kp1 is not None and kp2 is not None and match_count >= 4:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if mask is not None:
            inliers = int(mask.sum())
    return match_count, match_rate, inliers

def authenticate_image(input_image, match_thresh=15, rate_thresh=0.15, inlier_thresh=8):
    """
    画像（NumPy配列/BGR or グレースケール）を認証し、True/Falseを返す
    """
    if len(input_image.shape) == 3:
        input_img_gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    else:
        input_img_gray = input_image
    kp_input, des_input = extract_features(input_img_gray)

    db_images = load_database_images()
    for db_img in db_images:
        kp_db, des_db = extract_features(db_img)
        num_matches, match_rate, inliers = match_images(des_input, des_db, kp_input, kp_db)
        if num_matches >= match_thresh and match_rate >= rate_thresh and inliers >= inlier_thresh:
            return True  # 認証成功
    return False  # 認証失敗

# --- ここからFlaskエンドポイント追加 ---
app = Flask(__name__)

@app.route('/image_auth', methods=['POST'])
def image_auth():
    """
    フロントから画像データ（base64またはファイルアップロード）を受け取り、認証結果を返す
    """
    if 'image' in request.files:
        # ファイルアップロードの場合
        file = request.files['image']
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    elif request.is_json and 'image' in request.json:
        # base64エンコード画像の場合
        import base64
        from io import BytesIO
        image_data = base64.b64decode(request.json['image'].split(',')[1])
        img_array = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    else:
        return jsonify({'success': False, 'error': '画像データがありません'}), 400

    result = authenticate_image(img)
    return jsonify({'success': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)