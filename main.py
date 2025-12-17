import cv2
import numpy as np

CAM_INDEX = 0

def grab_frame(cap):
    ret, frame = cap.read()
    if not ret or frame is None:
        return None
    return frame

def nothing(x):
    pass

def main():
    cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)  # Windows 推荐
    if not cap.isOpened():
        raise RuntimeError("打不开摄像头：检查权限/编号/是否被占用")

    cv2.namedWindow("Control", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

    # OpenCV HSV: H 0~179, S 0~255, V 0~255
    cv2.createTrackbar("H_low",  "Control", 15, 179, nothing)
    cv2.createTrackbar("H_high", "Control", 40, 179, nothing)
    cv2.createTrackbar("S_low",  "Control", 80, 255, nothing)
    cv2.createTrackbar("S_high", "Control", 255, 255, nothing)
    cv2.createTrackbar("V_low",  "Control", 80, 255, nothing)
    cv2.createTrackbar("V_high", "Control", 255, 255, nothing)

    frozen = grab_frame(cap)
    if frozen is None:
        raise RuntimeError("读不到摄像头画面")

    while True:
        # 读滑块
        hL = cv2.getTrackbarPos("H_low", "Control")
        hH = cv2.getTrackbarPos("H_high","Control")
        sL = cv2.getTrackbarPos("S_low", "Control")
        sH = cv2.getTrackbarPos("S_high","Control")
        vL = cv2.getTrackbarPos("V_low", "Control")
        vH = cv2.getTrackbarPos("V_high","Control")

        # 保证 low <= high
        hL, hH = min(hL, hH), max(hL, hH)
        sL, sH = min(sL, sH), max(sL, sH)
        vL, vH = min(vL, vH), max(vL, vH)

        frame = frozen.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([hL, sL, vL], dtype=np.uint8)
        upper = np.array([hH, sH, vH], dtype=np.uint8)

        mask = cv2.inRange(hsv, lower, upper)

        # （可选）做一点形态学，让色块更干净
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # 去小噪点
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 填小孔洞

        cv2.putText(frame, "HSV thresholding | 'r': refresh | 'q': quit",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            new_frame = grab_frame(cap)
            if new_frame is not None:
                frozen = new_frame

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
