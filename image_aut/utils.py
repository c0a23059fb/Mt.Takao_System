import cv2
import numpy as np

def resize_image(image, size=(256, 256)):
    """画像を指定サイズにリサイズ"""
    return cv2.resize(image, size)

def denoise_image(image):
    """ノイズ除去（ガウシアンブラー）"""
    return cv2.GaussianBlur(image, (5, 5), 0)

def normalize_image(image):
    """画像を0-1に正規化"""
    return image.astype(np.float32) / 255.0

def crop_main_object(image):
    """画像から主なオブジェクト領域を自動で切り出す（最大輪郭抽出）"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return image  # 輪郭が見つからなければ元画像を返す
    # 最大輪郭を取得
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    cropped = image[y:y+h, x:x+w]
    return cropped