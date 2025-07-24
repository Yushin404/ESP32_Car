import cv2
import numpy as np
import requests
import time

# カメラ設定（OBS仮想カメラ or 通常カメラ）
cap = cv2.VideoCapture(0)
FRAME_W, FRAME_H = 1280, 720

# HSV範囲定義
COLOR_RANGES = {
    "red":   [([0, 100, 100],   [10, 255, 255]),
              ([160, 100, 100], [179, 255, 255])],
    "green": [([40,  50,  50],  [80, 255, 255])],
    "blue":  [([100, 150, 50],  [140, 255, 255])]
}
DRAW_COL = {"red": (0,0,255), "green": (0,255,0), "blue": (255,0,0)}

# ESP32 の IP アドレス
ESP32_HOST = "http://192.168.4.1"  # ESP32のIPに合わせて変更

last_command = None  # 前回送信したコマンド（連続送信防止）

def send_command(path):
    global last_command
    if path != last_command:
        try:
            requests.get(f"{ESP32_HOST}/{path}", timeout=0.3)
            print(f"Sent: {path}")
            last_command = path
        except Exception as e:
            print("送信失敗:", e)

def largest_centroid(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < 500:
        return None
    M = cv2.moments(c)
    if M["m00"] == 0: return None
    cx = int(M["m10"] / M["m00"])
    return cx

while True:
    ret, frame = cap.read()
    if not ret:
        print("映像取得失敗"); break

    frame = cv2.resize(frame, (FRAME_W, FRAME_H))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    positions = {}

    for color, ranges in COLOR_RANGES.items():
        mask_total = np.zeros((FRAME_H, FRAME_W), dtype=np.uint8)
        for lower, upper in ranges:
            mask_total |= cv2.inRange(hsv, np.array(lower), np.array(upper))
        cx = largest_centroid(mask_total)
        if cx is not None:
            norm_pos = (cx / FRAME_W) * 2 - 1  # 中心を0、左-1、右+1
            positions[color] = norm_pos
            # 可視化
            cv2.circle(frame, (cx, FRAME_H//2), 10, DRAW_COL[color], -1)
            cv2.putText(frame, f"{color}: {norm_pos:+.2f}",
                        (10, 30 + 30*list(COLOR_RANGES.keys()).index(color)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, DRAW_COL[color], 2)

    # 赤の位置に応じてコマンド送信
    if "red" in positions:
        pos = positions["red"]
        if abs(pos) < 0.5:
            send_command("forward")
        elif pos < 0:
            send_command("left")
        else:
            send_command("right")
    else:
        send_command("stop")

    cv2.imshow("Color Tracker", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESCで終了
        break

cap.release()
cv2.destroyAllWindows()
