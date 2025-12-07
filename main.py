import cv2

# 1. 打开默认摄像头 (索引 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

print("按 'q' 键退出程序")

while True:
    # 2. 逐帧捕获
    ret, frame = cap.read()

    # 如果读取失败（例如摄像头断开），则退出
    if not ret:
        print("无法接收画面 (流结束?). 退出中...")
        break

    # 3. 显示结果帧
    cv2.imshow('My Camera', frame)

    # 4. 按 'q' 键退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 5. 释放资源
cap.release()
cv2.destroyAllWindows()