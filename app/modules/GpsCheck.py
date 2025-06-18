import math

GPS = [
    (35.629841666666664, 139.25329),              # 浄心門
    (35.62639166666667, 139.25071666666668),       # 天狗の腰掛け杉付近の墓
    (35.625495, 139.25038333333333),               # 大本堂
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # 地球の半径（メートル）
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def is_within_radius(lat1, lon1, lat2, lon2, radius=150):
    return haversine(lat1, lon1, lat2, lon2) <= radius

def gps_checkpoint(lat, lon, gps_list=GPS, radius=150):
    for ref_lat, ref_lon in gps_list:
        if is_within_radius(lat, lon, ref_lat, ref_lon, radius):
            return True
    return False

# 使用例
# input_lat = 0
# input_lon = 0

# if gps_check(input_lat, input_lon):
#     print("150m以内に既知の地点があります。")
# else:
#     print("150m外です。")