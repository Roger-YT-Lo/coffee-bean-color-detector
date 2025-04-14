import cv2 as cv
import numpy as np
import os
import requests
#連接到ESP32-CAM ip
url="http://172.20.10.11:81/stream"
stream=requests.get(url, stream=True)

#初始化照片計數器
photo_counter = 0

#確保儲存圖片的目標資料夾存在
save_dir = "C:/Users/Asus/Desktop/CoffeeBeans/"
os.makedirs(save_dir, exist_ok=True)

#定義淺、中、灰顏色區間（HSV）
lower_light=np.array([10, 30, 90])    #HSV淺色範圍
upper_light=np.array([30, 150, 200])

lower_medium=np.array([10, 50, 40])  #HSV中等顏色範圍
upper_medium=np.array([35, 200, 80])

lower_dark=np.array([5, 50, 30])     #HSV深色範圍
upper_dark=np.array([35, 255, 50])

#定義濾除背景區間
lower_brown=np.array([3, 20, 25])    #下限
upper_brown=np.array([35, 180, 160]) #上限

for chunk in stream.iter_content(chunk_size=8192):
    # 找到 JPEG 影像的頭部和尾部
    jpghead = chunk.find(b'\xff\xd8')
    jpgend = chunk.find(b'\xff\xd9')
    if jpghead != -1 and jpgend != -1:
        img = chunk[jpghead:jpgend + 2]
        frame = cv.imdecode(np.frombuffer(img, np.uint8), cv.IMREAD_COLOR)
        if frame is not None:
            # 進行高斯模糊處理
            blurred_frame=cv.GaussianBlur(frame, (5, 5), 0)

            # 轉換為HSV顏色空間
            hsv_image=cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)

            # 建立咖啡豆範圍的遮罩
            mask=cv.inRange(hsv_image, lower_brown, upper_brown)
            # 篩選影像
            filtered_result=cv.bitwise_and(blurred_frame,blurred_frame,mask=mask)

            # 在影像中央畫一個十字定位點
            height, width, _=frame.shape
            center_x, center_y=width // 2, height // 2
            line_color=(0, 255, 0)  # 十字架顏色 (綠色)
            line_thickness=2
            # 在原始影像畫十字架
            cv.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), line_color, line_thickness)
            cv.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), line_color, line_thickness)
            # 在篩選後的影像畫十字架
            cv.line(filtered_result, (center_x - 10, center_y), (center_x + 10, center_y), line_color, line_thickness)
            cv.line(filtered_result, (center_x, center_y - 10), (center_x, center_y + 10), line_color, line_thickness)

            # 缺角檢測
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            has_corner = True  # 假設沒有缺角

            for contour in contours:
                # 計算輪廓的凸包
                convex_hull = cv.convexHull(contour)

                # 計算輪廓的面積與凸包面積
                contour_area = cv.contourArea(contour)
                convex_hull_area = cv.contourArea(convex_hull)

                # 計算輪廓面積與凸包面積的比值
                convexity_ratio = contour_area / convex_hull_area if convex_hull_area != 0 else 1
                cv.drawContours(frame, [convex_hull], -1, (0, 0, 255), 2)  # 紅色框出缺角

            # 顯示篩選後的影像
            cv.imshow("Filtered Coffee Beans", filtered_result)
            # 顯示原始影像
            cv.imshow("ESP32-CAM", frame)


            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):  # 按下 'q' 結束程式
                break
            elif key == ord('a'):  # 按下 'a' 拍照並儲存圖片
                photo_counter += 1
                photo_path = os.path.join(save_dir, f"coffee_photo_{photo_counter}.jpg")
                if not cv.imwrite(photo_path, frame):
                    print(f"無法儲存圖片至: {photo_path}")
                else:
                    print(f"照片已儲存至: {photo_path}")
            elif key == ord('s'):  # 按下 's' 顯示中央 HSV 值並辨識顏色範圍
                # 獲取中央像素的 HSV 值
                hsv_center = hsv_image[center_y, center_x]
                hue, saturation, value = hsv_center

                # 終端機顯示 HSV 值
                print(f"中央點的 HSV 值：H={hue}, S={saturation}, V={value}")

                # 建立不同範圍的遮罩
                mask_light = cv.inRange(hsv_image, lower_light, upper_light)
                mask_medium = cv.inRange(hsv_image, lower_medium, upper_medium)
                mask_dark = cv.inRange(hsv_image, lower_dark, upper_dark)

                # 計算每個遮罩的白色像素（表示匹配的範圍大小）
                count_light = cv.countNonZero(mask_light)
                count_medium = cv.countNonZero(mask_medium)
                count_dark = cv.countNonZero(mask_dark)

                # 判斷哪個範圍最大
                if count_light > count_medium and count_light > count_dark:
                    print("偵測結果：淺色咖啡豆")
                elif count_medium > count_light and count_medium > count_dark:
                    print("偵測結果：中等顏色咖啡豆")
                elif count_dark > count_light and count_dark > count_medium:
                    print("偵測結果：深色咖啡豆")
                else:
                    print("無法確定顏色（可能顏色區間需要調整）")

cv.destroyAllWindows()
