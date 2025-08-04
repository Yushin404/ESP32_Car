import cv2
import numpy as np

##=== 適宜変更する！！ ===##
cap = cv2.VideoCapture("http://10.146.137.194:8080/video")

FRAME_W, FRAME_H = 640, 480

# LAB色空間の範囲（OpenCVでは A*,B* は 0〜255）
# 実際の布に応じてチューニングしてください
color_ranges = {
    "red":   ([  0, 160,   0], [255, 255, 150]),   # A*高め & B*中程度
    "green": ([  0,  70,  80], [255, 150, 180]),   # A*中程度 & B*中
    "blue":  ([  0,  90,   0], [255, 140, 130])    # B*低め & A*中程度
}

while True:
    ret, frame = cap.read()
    if not ret:
        print("映像取得できません")
        break

    # リサイズ
    frame = cv2.resize(frame, (FRAME_W, FRAME_H))

    # BGR → LAB変換
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # 各色マスク
    mask_red   = cv2.inRange(lab, np.array(color_ranges["red"][0]),   np.array(color_ranges["red"][1]))
    mask_green = cv2.inRange(lab, np.array(color_ranges["green"][0]), np.array(color_ranges["green"][1]))
    mask_blue  = cv2.inRange(lab, np.array(color_ranges["blue"][0]),  np.array(color_ranges["blue"][1]))

    # 各色の抽出画像を作成
    result_red   = cv2.bitwise_and(frame, frame, mask=mask_red)
    result_green = cv2.bitwise_and(frame, frame, mask=mask_green)
    result_blue  = cv2.bitwise_and(frame, frame, mask=mask_blue)

    # 表示
    cv2.imshow("Original", frame)
    cv2.imshow("Red (LAB)", result_red)
    cv2.imshow("Green (LAB)", result_green)
    cv2.imshow("Blue (LAB)", result_blue)

    if cv2.waitKey(1) & 0xFF == 27:  # ESCで終了
        break

cap.release()
cv2.destroyAllWindows()
