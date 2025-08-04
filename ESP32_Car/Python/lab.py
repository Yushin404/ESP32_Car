import cv2
import numpy as np

##=== 適宜変更する！！ ===##
cap = cv2.VideoCapture("http://10.146.137.194:8080/video")

FRAME_W, FRAME_H = 640, 480

# -------- LAB 版しきい値 --------
#  OpenCV の LAB は 0-255 スケール (A*,B* は +128 シフト)
#  ここでは「そこそこ彩度が高い布」を想定した例
COLOR_RANGES = {
    "red":   [([  0, 160,   0], [255, 255, 140])],   # A* が 160 以上, B* 140 以下
    "green": [([  0,  40,  80], [255, 140, 200])],   # A* 40-140, B* 80-200
    "blue":  [([  0,  80,   0], [255, 170, 120])]    # B* が小さめ & A* 中央
}
DRAW_COL = {"red": (0,0,255), "green": (0,255,0), "blue": (255,0,0)}

def largest_centroid(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < 500:
        return None
    M = cv2.moments(c)
    if M["m00"] == 0: return None
    return int(M["m10"] / M["m00"])

while True:
    ret, frame = cap.read()
    if not ret:
        print("映像取得失敗"); break
    frame = cv2.resize(frame, (FRAME_W, FRAME_H))

    # -------- BGR → LAB へ変換 --------
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    positions = {}

    for color, ranges in COLOR_RANGES.items():
        mask_total = np.zeros((FRAME_H, FRAME_W), dtype=np.uint8)
        for lower, upper in ranges:
            mask_total |= cv2.inRange(lab, np.array(lower, np.uint8),
                                           np.array(upper, np.uint8))
        cx = largest_centroid(mask_total)
        if cx is not None:
            norm_pos = (cx / FRAME_W) * 2 - 1
            positions[color] = norm_pos
            cv2.circle(frame, (cx, FRAME_H//2), 10, DRAW_COL[color], -1)
            cv2.putText(frame, f"{color}: {norm_pos:+.2f}",
                        (10, 30 + 30*list(COLOR_RANGES.keys()).index(color)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, DRAW_COL[color], 2)

    print({c: f"{p:+.2f}" for c, p in positions.items()}, end="\r", flush=True)

    cv2.imshow("IP Webcam LAB Color Tracker", frame)
    if cv2.waitKey(1) & 0xFF == 27:   # ESC で終了
        break

cap.release()
cv2.destroyAllWindows()
